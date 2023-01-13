from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask import current_app as app
from flask_login import login_user, current_user, logout_user, login_required
from application.models import User
from application.database import *
from application.validation import signupForm, loginForm, profileForm

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = loginForm()
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return render_template('login.html', title = 'Login', form = form)
    try:        
        if form.validate_on_submit():
            user = User.query.filter_by(user_name = form.user_name.data).first()
            if user and (user.password == form.password.data):
                login_user(user)     
                flash('User login successful.', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login unsuccessful please try with correct username and password', 'danger')
        
        return render_template('login.html', title = 'Login', form = form)
    except Exception as err:
        flash(err, 'danger')
        return render_template('login.html', title = 'Login', form = form)

    
@app.route("/signup", methods = ["GET", "POST"])
def signup():
    form = signupForm()
    if request.method == 'GET':
        return render_template('signup.html', title = 'Signup', form = form)
    else:
        try:
            if form.validate_on_submit():
                user = User(user_name=form.user_name.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('Your account has been created! You are now able to log in', 'success')
                return redirect(url_for('login'))#render_template('signup.html', title = 'Signup', form = form)
            else:
                return render_template('signup.html', title = 'Signup', form = form)
        except Exception as err:
            db.session.rollback()
            flash(err, 'danger')
            return render_template('signup.html', title = 'Signup', form = form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/profile", methods = ['GET', 'POST'])
@login_required
def profile():
    profile_pic = url_for('static', filename='images/'+ current_user.profile_pic)
    form = profileForm()    
    # if request.method == 'GET':
    #     form.user_name.data = current_user.user_name
    #     form.first_name.data = current_user.first_name
    #     form.last_name.data = current_user.last_name
    #     form.email.data = current_user.email
    #     return render_template('profile.html', title = 'Profile', form = form, profile_pic = profile_pic)
    # else:
    #     try:
    #         print(form.validate_on_submit())
    #         if form.validate_on_submit():
    #             current_user.user_name = form.user_name.data
    #             current_user.first_name = form.first_name.data
    #             current_user.last_name = form.last_name.data
    #             current_user.email = form.email.data
    #             db.session.commit()
    #             flash('Account details updated successfully.', 'success')
    #             return render_template('profile.html', title='Profile', form = form, profile_pic = profile_pic)
    #         else:
    #             flash('Please try again.', 'info')
    #             return render_template('profile.html', title='Profile', form = form, profile_pic = profile_pic)
                
    #     except Exception as err:
    #         db.session.rollback()
    #         flash(err, 'danger')
    #         return render_template('profile.html', title='Profile', form = form, profile_pic = profile_pic)
    if form.validate_on_submit():
        try:
            current_user.user_name = form.user_name.data
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Account details updated successfully.', 'success')
            return render_template('profile.html', title='Profile', form = form, profile_pic = profile_pic)
        # else:
        #     return render_template('profile.html', title='Profile', form = form, profile_pic = profile_pic)
            
        except Exception as err:
            flash('Please try again.', 'info')
            db.session.rollback()
            flash(err, 'danger')
            return render_template('profile.html', title='Profile', form = form, profile_pic = profile_pic)
    elif request.method == 'GET':
        form.user_name.data = current_user.user_name
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        return render_template('profile.html', title = 'Profile', form = form, profile_pic = profile_pic)
    
    return render_template('profile.html', title='Profile', form = form, profile_pic = profile_pic)

