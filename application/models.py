from flask_sqlalchemy import SQLAlchemy
from application.database import db, ma, login_manager
from flask_login import UserMixin, current_user
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True, index = True)
    user_name = db.Column(db.String, unique = True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    profile_pic = db.Column(db.String, default = "default.jpg")
    password = db.Column(db.String)
    followers = db.Column(db.Integer, default = 0)
    following = db.Column(db.Integer, default = 0)
    posts = db.Column(db.Integer, default = 0)
    blogs = db.relationship('Blog', backref='user', lazy = True)

    def __init__(self, user_name, first_name, last_name, email, password):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
    
    def get_id(self):
           return (self.user_id)

class userSchema(ma.Schema):
    class meta:
        fields = ('user_name', 'first_name', 'last_name', 'email', 'password')

user_schema = userSchema()
users_schema = userSchema(many = True)

class Blog(db.Model):
    __tablename = 'blog'
    blog_id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True, index = True)
    blog_title = db.Column(db.String)
    blog_body = db.Column(db.String)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)

    def __repr__(self):
        return f"Blog('{self.blog_title}', '{self.created_at}')"

class Follower(db.Model):
    __tablename__ = 'follower'
    follower_id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True, index = True)
    follower_user_id = db.Column(db.Integer)
    follower_user_name = db.Column(db.String)
    user_id = db.Column(db.Integer)

class Following(db.Model):
    __tablename__ = 'following'
    following_id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True, index = True)
    following_user_id = db.Column(db.Integer)
    following_user_name = db.Column(db.String)
    user_id = db.Column(db.Integer)







