import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api 
from dotenv import load_dotenv
from application.config import LocalDevelopmentConfig
from application.database import db, ma
# from userController import *
load_dotenv()

app = Flask(__name__,  template_folder = "templates")

app.config.from_object(LocalDevelopmentConfig)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY 
db.init_app(app)
ma.init_app(app)
api = Api(app)
app.app_context().push() 

from application.api.userApi import userApi
api.add_resource(userApi, "/api/v1/user")

db.create_all()

from application.controller.userController import *

@app.route('/', methods = ['GET'])
@app.route('/home', methods = ['GET'])
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True, port = 8080)

