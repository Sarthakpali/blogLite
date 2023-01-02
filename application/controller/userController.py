from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask import current_app as app
from application.models import user_schema, users_schema, userSchema, User
from application.database import *
from application.validation import signupForm

@app.route("/login", methods = ["GET"])
def userLogin():

    return "Login Page"

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    form = signupForm()
    if request.method == 'GET':
        return render_template('signup.html', title = 'Signup', form = form)
    else:
        # print(form.validate_on_submit())
        try:
            if form.validate_on_submit():
                # print(form.user_name)
                user = User(user_name=form.user_name.value, first_name=form.first_name.value, last_name=form.last_name.value, email=form.email.value, password=form.password.value)
                print("Hello")
                print(user)
                return render_template('signup.html', title = 'Signup', form = form)
                
            else: 
                print("Hello else")
                return render_template('signup.html', title = 'Signup', form = form)
        except Exception as err:
            # db.session.rollback()
            return erru
            ret