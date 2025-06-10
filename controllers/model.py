from controllers.database import db 

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(80),nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    password=db.Column(db.String(50),nullable=False)
    address=db.Column(db.String(120),nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    is_admin=db.Column(db.Boolean,default=False)
    
'''class Role(db.model):
    id=db.column(db.integer,primary_key=True,autoincrement=True)
    name=db.column(db.string(50),nullable=True)

class user_role(db.model):
    id=db.column(db.integer,primary_key=True,autoincrement=True)
    user_id=db.column(db.integer,foreign_key=('user.id'))
    role_id=db.column(db.integer,foreign_key=('role.id'))
'''

