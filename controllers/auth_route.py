from app import app
from flask import render_template,request,url_for,redirect,session
from flask_login import login_user, logout_user, login_required
from controllers.model import User
from controllers.database import db

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            print("please fill email and password")

        if "@" not in email:
            print("invalid email")

        find1 = User.query.filter_by(email=email).first()
        if not find1:
            return render_template('login.html')
        
        if find1.password != password:
            return render_template('login.html')
        
        login_user(find1)
        
        if find1.password == password:
            if find1.is_admin:
                return redirect('/admin')
            else:
                user_id=find1.id
                return redirect(url_for('user_dashboard',user_id=find1.id))
        
    return render_template("login.html")
           
@app.route("/sign-up",methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        formname = request.form.get('name')
        formpassword = request.form.get('password')
        formemail = request.form.get('email')
        formaddress = request.form.get('address')
        formpincode = request.form.get('pincode')
        user = User(name=formname,
                     password=formpassword,
                     email=formemail,
                     address=formaddress,
                     pincode=formpincode)
        db.session.add(user)
        db.session.commit()
        print('User added')
        return redirect('/login')
    return render_template("create_account.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))