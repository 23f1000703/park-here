from app import app
from flask import render_template,request,url_for,redirect,flash,session
from controllers.model import User,ParkingLot,ParkingSpot
from controllers.database import db


@app.route("/admin")
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
def delete_lot(id):
    lot = ParkingLot.query.get_or_404(id)
    db.session.delete(lot)
    db.session.commit()
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/spot/<int:id>")
def spot_detail(id):
    spot = ParkingSpot.query.get_or_404(id)
    return render_template("spot_detail.html", spot=spot)

@app.route("/admin/delete_spot/<int:id>",methods=["GET","POST"])
def delete_spot(id):
    spot = ParkingSpot.query.get_or_404(id)
    if spot.is_occupied:
        return "Cannot delete occupied spot."
    db.session.delete(spot)
    db.session.commit()
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/summary")
def summary():
    lots = ParkingLot.query.all()
    return render_template("summary.html", lots=lots)