from app import app
from flask import render_template,request,url_for,redirect,session
from controllers.model import User,ParkingLot,ParkingSpot,ParkingHistory
from controllers.database import db
from datetime import datetime
import matplotlib.pyplot as plt
from flask_login import login_required
import os

@app.route("/user/dashboard/<int:user_id>", methods=["GET", "POST"])
@login_required
def user_dashboard(user_id):
    user = User.query.get(user_id)

    search = request.args.get('search')
    if search:
        lots = ParkingLot.query.filter(ParkingLot.address.ilike(f"%{search}%") | ParkingLot.pincode.ilike(f"%{search}%")).all()
    else:
        lots = ParkingLot.query.all()
    
    for lot in lots:
        total_spots = len(lot.spots)
        occupied_spots = int(0)
        for spot in lot.spots:
            if spot.is_occupied:
                occupied_spots = occupied_spots + int(1)
        lot.capacity = total_spots
        lot.occupied = occupied_spots
        lot.remain_spot = lot.capacity-lot.occupied
 
    history = ParkingSpot.query.filter_by(customer_id=user.id).filter(ParkingSpot.time_in != None).order_by(ParkingSpot.time_in.desc()).all()
    return render_template("user_dashboard.html", user=user, lots=lots, history=history)


@app.route("/user/book/<int:user_id>/<int:lot_id>", methods=["GET", "POST"])
@login_required
def book_spot(user_id, lot_id):
    user = User.query.get(user_id)
    lot = ParkingLot.query.get(lot_id)

    # Find the first unoccupied spot in this lot
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, is_occupied=False).first()

    if not spot:
        return "No available spot in this lot."

    if request.method == "POST":
        vehicle_number = request.form.get("vehicle_number")
        if not vehicle_number:
            return render_template("book_spot.html",spot=spot, user=user)

        spot.customer_id = user.id
        spot.vehicle_number = vehicle_number
        spot.is_occupied = True
        spot.time_in = datetime.now()
        db.session.commit()
        return redirect(url_for('user_dashboard', user_id=user_id))

    return render_template("book_spot.html", spot=spot, user=user)


@app.route("/user/release/<int:user_id>/<int:spot_id>",methods=["GET","POST"])
@login_required
def release_spot(user_id, spot_id):
    spot = ParkingSpot.query.get(spot_id)
    time_in = spot.time_in
    time_out = datetime.now()
    hours = 1+((time_out-time_in).total_seconds() // 3600)
    cost = hours*spot.lot.price_per_hour
    

    history = ParkingHistory(
        user_id=user_id,
        lot_name=spot.lot.name,
        lot_address=spot.lot.address,
        spot_id=spot.id,
        vehicle_number=spot.vehicle_number,
        time_in=time_in.strftime('%Y-%m-%d %I:%M %p'),
        time_out=time_out.strftime('%Y-%m-%d %I:%M %p'),
        cost=cost
    )
    db.session.add(history)

    if request.method == "POST":
        spot.is_occupied = False
        spot.cost = cost
        spot.time_in = None
        spot.customer_id = None
        spot.vehicle_number = None  # optional: if stored
        db.session.commit()
        return redirect( url_for("user_dashboard",user_id=user_id) )
    return render_template("release_spot.html", spot=spot, time_out=time_out, cost=cost)

@app.route("/user/history/<int:user_id>")
@login_required
def history(user_id):
    history = ParkingHistory.query.filter_by(user_id=user_id).all()
    return render_template("history.html",history=history,user_id=user_id)

@app.route("/user/edit/<int:user_id>",methods=["GET","POST"])
@login_required
def edit_profile(user_id):
    user=User.query.get(user_id)
    if request.method =="POST":
        user.name=request.form['name']
        user.email=request.form['email']
        user.address=request.form['address']
        user.pincode=request.form['pincode']
        db.session.commit()
        return redirect(url_for('user_dashboard',user_id=user.id))    
    return render_template('edit_profile.html',user=user)

@app.route("/user/summary/<int:user_id>")
@login_required
def user_summary(user_id):
    history = ParkingHistory.query.filter_by(user_id=user_id).all()
    lot_time={}

    for record in history:
        if record.time_in and record.time_out:
            # Convert string to datetime
            time_in = datetime.strptime(record.time_in, "%Y-%m-%d %I:%M %p")
            time_out = datetime.strptime(record.time_out, "%Y-%m-%d %I:%M %p")
            
            hours = (time_out - time_in).total_seconds() / 3600

            # Add hours to the respective lot
            if record.lot_name in lot_time:
               lot_time[record.lot_name] += hours 
            else:
              lot_time[record.lot_name] = hours


    spot_ids = list(lot_time.keys())
    revenues = list(lot_time.values())

    plt.figure(figsize=(8, 5))
    plt.bar([str(sid) for sid in spot_ids], revenues, color='skyblue')
    plt.xlabel("Spot Name")
    plt.ylabel("No. of Time Spent(Hours)")
    plt.title("Most Visited Parking Spot")
    plt.tight_layout()
    plt.savefig("static/user_booking.jpg")
    plt.clf()

    return render_template("user_summary.html",user_id=user_id)