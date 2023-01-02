from flask_sqlalchemy import SQLAlchemy
from application.database import db
from application.database import ma

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True, index = True)
    user_name = db.Column(db.String, unique = True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    followers = db.Column(db.Integer, default = 0)
    following = db.Column(db.Integer, default = 0)
    posts = db.Column(db.Integer, default = 0)

    def __init__(self, user_name, first_name, last_name, email, password):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

class userSchema(ma.Schema):
    class meta:
        fields = ('user_name', 'first_name', 'last_name', 'email', 'password')

user_schema = userSchema()
users_schema = userSchema(many = True)




