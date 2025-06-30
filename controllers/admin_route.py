from app import app
from flask import render_template,request,url_for,redirect,session
from flask_login import login_required
from controllers.model import User,ParkingLot,ParkingSpot,ParkingHistory
from controllers.database import db
from datetime import datetime
import matplotlib.pyplot as plt
import os


@app.route("/admin")
@login_required
def admin_dashboard():
    lots = ParkingLot.query.all()
    for lot in lots:
        total_spots = len(lot.spots)
        occupied_spots = int(0)
        for spot in lot.spots:
            if spot.is_occupied:
                occupied_spots = occupied_spots + int(1)
        lot.capacity = total_spots
        lot.occupied = occupied_spots
    return render_template("admin_dashboard.html", lots=lots)

@app.route("/admin/add_lot", methods=["GET", "POST"])
@login_required
def add_lot():
    if request.method == "POST":
        lot = ParkingLot(
            name=request.form['name'],
            address=request.form['address'],
            pincode=request.form['pincode'],
            price_per_hour=request.form['price'],
            max_spots=request.form['max_spots']
        )
        db.session.add(lot)
        db.session.commit()
        for i in range(int(lot.max_spots)):
            db.session.add(ParkingSpot(lot_id=lot.id))
        db.session.commit()
        return redirect(url_for("admin_dashboard"))
    return render_template("add_lot.html")

@app.route("/admin/edit_lot/<int:id>", methods=["GET", "POST"])
@login_required
def edit_lot(id):
    lot = ParkingLot.query.get_or_404(id)

    if request.method == "POST":
        lot.name = request.form['name']
        lot.address = request.form['address']
        lot.pincode = request.form['pincode']
        lot.price_per_hour = float(request.form['price'])

        new_max_spots = int(request.form['max_spots'])
        old_max_spots = lot.max_spots
        current_spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()

        if new_max_spots > old_max_spots:
            # Add new empty spots
            for _ in range(new_max_spots - old_max_spots):
                new_spot = ParkingSpot(lot_id=lot.id)
                db.session.add(new_spot)

        elif new_max_spots < old_max_spots:
            # Remove unoccupied spots if needed
            empty_spots = [spot for spot in current_spots if not spot.is_occupied]
            to_remove = old_max_spots - new_max_spots

            if len(empty_spots) >= to_remove:
                for spot in empty_spots[:to_remove]:
                    db.session.delete(spot)
            else:
                return "Cannot reduce spots: not enough empty spots to delete."

        lot.max_spots = new_max_spots
        db.session.commit()
        return redirect(url_for("admin_dashboard"))

    return render_template("edit_lot.html", lot=lot)

@app.route("/admin/delete_lot/<int:id>")
@login_required
def delete_lot(id):
    lot = ParkingLot.query.get_or_404(id)
    db.session.delete(lot)
    db.session.commit()
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/spot/<int:id>")
@login_required
def spot_detail(id):
    spot = ParkingSpot.query.get_or_404(id)
    customer = User.query.get(spot.customer_id)
    return render_template("spot_detail.html", spot=spot, customer=customer)

@app.route("/admin/detail/<int:id>")
@login_required
def detail(id):
    spot = ParkingSpot.query.get(id)
    customer = User.query.get(spot.customer_id)
    time_in=spot.time_in
    time_out=datetime.now()
    hours = 1+((time_out-time_in).total_seconds() // 3600)
    spot.cost = hours*spot.lot.price_per_hour
    
    return render_template("occupied_spot_detail.html",spot=spot,customer=customer)

@app.route("/admin/delete_spot/<int:id>",methods=["GET","POST"])
@login_required
def delete_spot(id):
    spot = ParkingSpot.query.get(id)
    if spot.is_occupied:
        return "Cannot delete occupied spot."
    db.session.delete(spot)
    db.session.commit()
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/user")
@login_required
def reg_user():
    users=User.query.all()
    return render_template("reg_user.html",users=users)

@app.route("/admin/edit",methods=["GET","POST"])
@login_required
def edit_admin_profile():
    user=User.query.get(1)
    if request.method =="POST":
        user.name=request.form['name']
        user.email=request.form['email']
        user.address=request.form['address']
        user.pincode=request.form['pincode']
        db.session.commit()
        return redirect(url_for('admin_dashboard'))    
    return render_template('edit_admin_profile.html',user=user)

@app.route("/admin/search", methods=["GET", "POST"])
@login_required
def admin_search():
    search_type = request.form.get("search_type")
    query = request.form.get("search_query")
    user_results = []
    lot_results = []

    if request.method == "POST":
        if search_type == "user_id" and query.isdigit():
            user = User.query.filter_by(id=int(query)).first()
            if user:
                user_results.append(user)

        elif search_type == "location":
            lot_results = ParkingLot.query.filter(ParkingLot.address.ilike(f"%{query}%")).all()

        elif search_type == "user_email":
            user = User.query.filter(User.email.ilike(f"%{query}%")).first()
            if user:
                user_results.append(user)

        elif search_type == "user_name":
            users = User.query.filter(User.name.ilike(f"%{query}%")).all()
            user_results.extend(users)

        elif search_type == "pincode":
            lot_results = ParkingLot.query.filter(ParkingLot.pincode == query).all()

    return render_template("admin_search.html", user_results=user_results, lot_results=lot_results)


@app.route("/admin/summary")
@login_required
def summary():
    history = ParkingHistory.query.all()

    from collections import Counter

    lot_counts = Counter([record.lot_name for record in history])
    labels = list(lot_counts.keys())
    sizes = list(lot_counts.values())

    plt.figure(figsize=(6, 6))
    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        wedgeprops={'width': 0.4},
        textprops={'color': 'black'}
    )
    plt.title("Booking Distribution by Parking Lot")

    
    plt.tight_layout()
    plt.savefig("static/booking_pie.jpg")
    plt.clf()

    spot_revenue = {}
    for record in history:
        spot_id = record.lot_name
        spot_revenue[spot_id] = spot_revenue.get(spot_id, 0) + record.cost

    spot_ids = list(spot_revenue.keys())
    revenues = list(spot_revenue.values())

    plt.figure(figsize=(8, 5))
    plt.bar([str(sid) for sid in spot_ids], revenues, color='skyblue')
    plt.xlabel("Spot ID")
    plt.ylabel("Revenue (₹)")
    plt.title("Revenue Generated by Parking Spot")
    plt.tight_layout()
    plt.savefig("static/spot_revenue.jpg")
    plt.clf()

    return render_template("summary.html")