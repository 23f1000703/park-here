from flask import Flask,render_template,request,url_for
from controllers.database import db
from controllers.config import config
from controllers.model import User



app = Flask(__name__)
app.config.from_object(config)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Parking_services.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

def create_admin():
    if_exist = User.query.filter_by(is_admin=True).first()
    if not if_exist:
        admin = User(name='admin',
                     password='admin12345',
                     email='admin12345@gmail.com',
                     address='admin location',
                     pincode='800002',
                     is_admin=True)
        db.session.add(admin)
        db.session.commit()



@app.route("/")
def home():
    return render_template("homepage.html")

from controllers.auth_route import *

if __name__ == "__main__" :
    with app.app_context():  # This ensures app context is active for DB query
        create_admin()
    app.run(debug=True)
