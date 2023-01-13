from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, abort
from flask import current_app as app
from flask_login import login_user, current_user, logout_user, login_required
from application.models import Blog
from application.database import *
from application.validation import blogForm, editblogForm

@app.route('/newBlog', methods = ["GET", "POST"])
@login_required
def newBlog():
    form = blogForm()
    if request.method == 'GET':
        return render_template('newBlog.html', title = 'New Blog', form = form)
    else:
        try:
            if form.validate_on_submit():
                # print("H")
                blog = Blog(blog_title = form.blog_title.data, blog_body = form.blog_body.data, user = current_user)
                db.session.add(blog)
                db.session.commit()
                flash('New blog posted successfully.', 'success')
                return redirect(url_for('home'))
            else:
                flash('Please try again.', 'info')
                return render_template('newBlog.html', title = 'New Blog', form = form)
        except Exception as err:
            flash(err, 'danger')
            return render_template('newBlog.html', title = 'New Blog', form = form)

@app.route('/editBlog/<int:blog_id>', methods = ["GET", "POST"])
@login_required
def editBlog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if blog.user != current_user:
        flash('You are not authorised to edit this blog.', 'danger')
        abort(403)
    form = editblogForm()
    if request.method == 'GET':
        form.blog_title.data = blog.blog_title
        form.blog_body.data = blog.blog_body
        return render_template('editBlog.html', title = 'Edit Blog', form = form)
    else:
        try:
            if form.validate_on_submit():
                blog.blog_title = form.blog_title.data
                blog.blog_body = form.blog_body.data
                db.session.commit()
                flash('Blog edited successfully.', 'success')
                return redirect(url_for('blog', blog_id = blog.blog_id))
        except Exception as err:
            db.session.rollback()
            flash(err, 'danger')
            return render_template('editBlog.html', title = 'Edit Blog', form = form)

@app.route('/deleteBlog/<int:blog_id>')
@login_required
def deleteBlog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if blog.user != current_user:
        flash('You are not authorised to delete this blog.', 'danger')
        abort(403)
    try:
        db.session.delete(blog)
        db.session.commit()
        flash('Blog deleted successfully.', 'success')
        return redirect(url_for('home'))
    except Exception as err:
        db.session.rollback()
        flash(err, 'danger')
        return redirect(url_for('home'))


@app.route('/blog/<int:blog_id>')
def blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    return render_template('blog.html', title = blog.blog_title, blog = blog)



