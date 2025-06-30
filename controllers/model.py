from controllers.database import db 
from datetime import datetime
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(80),nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    password=db.Column(db.String(50),nullable=False)
    address=db.Column(db.String(120),nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    is_admin=db.Column(db.Boolean,default=False)
    
class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    pincode = db.Column(db.String(10))
    price_per_hour = db.Column(db.Float)
    max_spots = db.Column(db.Integer)
    spots = db.relationship('ParkingSpot', backref='lot', cascade='all, delete-orphan')

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_occupied = db.Column(db.Boolean, default=False)
    customer_id = db.Column(db.Integer, nullable=True)
    vehicle_number = db.Column(db.String(20), nullable=True)
    time_in = db.Column(db.DateTime, nullable=True)
    cost = db.Column(db.Float, nullable=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'))

class ParkingHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    lot_name = db.Column(db.String(50))
    lot_address = db.Column(db.String(200))
    spot_id= db.Column(db.Integer)
    vehicle_number = db.Column(db.String(20))
    time_in = db.Column(db.String(20))
    time_out = db.Column(db.String(20))
    cost = db.Column(db.Float)
