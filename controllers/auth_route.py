from app import app
from flask import render_template,request,url_for,redirect,flash,session
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
            flash("YOUR DETAIL NOT MATCHED")
            return render_template('login.html')
        
        if find1.password != password:
            flash("Invalid password")
            return render_template('login.html')
        
        session['user_id'] = find1.id
        session['email_id'] = find1.email
        session['is_admin'] = find1.is_admin
        
        if find1.password == password:
            if find1.is_admin:
                return render_template('admin_dashboard.html')
            else:
                return render_template('user_dashboard.html')
        
    return render_template("login.html")
           
@app.route("/sign-up",methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        formname = request.form.get('name')
        formpassword = request.form.get('password')
        formemail = request.form.get('email')
        formaddress = request.form.get('address')
        formpincode = request.form.get('pincode')
        user = user(name=formname,
                     password=formpassword,
                     email=formemail,
                     address=formaddress,
                     pincode=formpincode)
        db.session.add(user)
        db.session.commit()
        print('User added')
        return redirect('/login')
    return render_template("create_account.html")