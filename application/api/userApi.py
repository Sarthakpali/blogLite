from flask import request
from flask_restful import Resource, marshal_with, fields, reqparse
from application.models import User
from application.database import db

data_fields = {
    'user_id': fields.Integer,
    'user_name': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'password': fields.String,    
}

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('user_name')
create_user_parser.add_argument('first_name')
create_user_parser.add_argument('last_name')
create_user_parser.add_argument('email')
create_user_parser.add_argument('password')

class userApi(Resource):   
    @marshal_with(data_fields)
    def post(self):
            args = create_user_parser.parse_args(strict = True)
            user_name = args.get("user_name", None)
            first_name = args.get("first_name", None)
            last_name = args.get("last_name", None)
            email = args.get("email", None)
            password = args.get("password", None)
            
            user = User(user_name = user_name, first_name = first_name, last_name = last_name, email = email, password = password)
            print(user)
            
            db.session.add(user)
            db.session.commit()
           
            return user

        