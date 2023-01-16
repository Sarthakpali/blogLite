import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask import current_app as app
from flask_login import login_user, current_user, logout_user, login_required
from application.models import User, Follower
from application.database import *
from application.validation import signupForm, loginForm, profileForm, searchForm, followForm

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

@app.route("/profile", methods = ["GET", "POST"])
def profile():
    profile_pic = url_for('static', filename='images/' + current_user.profile_pic)
    form = profileForm()
    if request.method == 'GET':
        form.user_name.data  = current_user.user_name
        form.first_name.data  = current_user.first_name
        form.last_name.data  = current_user.last_name
        form.email.data = current_user.email
        return render_template('profile.html', title = 'Profile', form = form, profile_pic = profile_pic)
    else:
        try:
            if form.validate_on_submit():
                if form.profile_pic.data:
                    # print(app.root_path)
                    # paths = app.root_path+'/static/images/'+form.profile_pic.data
                    # print(type(app.root_path))
                    # print(type(form.profile_pic.data))
                    # print(paths)
                    path_pic = os.path.join(app.root_path, 'static/images', form.profile_pic.data)
                    form.profile_pic.data.save(path_pic)
                    current_user.profile_pic = form.profile_pic.data
                current_user.user_name = form.user_name.data
                current_user.first_name = form.first_name.data
                current_user.last_name = form.last_name.data
                current_user.email = form.email.data
                db.session.commit()
                flash('Profile updated successfully', 'success')
                return redirect(url_for('profile'))
            else:
                flash('Something went wrong, please try again.', 'info')
                return redirect(url_for('profile'))

        except Exception as err:
            db.session.rollback()
            flash(err, 'danger')
            return render_template('profile.html',  title = 'Profile', form = form, profile_pic = profile_pic)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.context_processor
def layout():
    form = searchForm()
    return dict(form = form)

@app.route("/search", methods=["POST"])
def search():
    form = searchForm()
    if form.validate_on_submit():
        users = User.query.filter(User.user_name.like('%'+form.search.data+'%'))
        return render_template('search.html', title="Search", form = form, users = users)
    else:
        return render_template('search.html', title="Search", form = form)

@app.route("/user/<int:user_id>")
def user(user_id):
    user = User.query.get_or_404(user_id)
    profile_pic = url_for('static', filename='images/' + user.profile_pic)
    form = profileForm()
    form_u = followForm()
    print(form_u)
    if current_user and (user == current_user):
        form.user_name.data  = current_user.user_name
        form.first_name.data  = current_user.first_name
        form.last_name.data  = current_user.last_name
        form.email.data = current_user.email
        return render_template('profile.html',  title = 'Profile', form = form, profile_pic = profile_pic)
    title = user.first_name.capitalize()+" "+user.last_name.capitalize()
    return render_template('user.html', title = title, user = user, form = form_u)

@app.route('/deleteUser/<int:user_id>')
@login_required
def deleteUser(user_id):
    user = User.query.get_or_404(user_id)
    if user != current_user:
        flash('You are not authorised to delete this account.', 'danger')
        abort(403)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('Your account has been deleted successfully.', 'success')
        return redirect(url_for('home'))
    except Exception as err:
        db.session.rollback()
        flash(err, 'danger')
        return redirect(url_for('home'))

    

