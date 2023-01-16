from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import User, Blog


class signupForm(FlaskForm):
    user_name = StringField('user_name', validators=[DataRequired()])
    email = StringField('email',validators=[DataRequired(), Email()])
    first_name = StringField('first_name',validators=[DataRequired()])
    last_name = StringField('last_name',validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_user_name(self, user_name):
        user = User.query.filter_by(user_name=user_name.data).first()
        if user:
            raise ValidationError('That username is not available, please select a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('An account already exists by this email, Please login.')


class loginForm(FlaskForm):
    user_name = StringField('user_name',validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
        
class profileForm(FlaskForm):
    user_name = StringField('user_name', validators=[DataRequired()])
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    profile_pic = FileField('update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_user_name(self, user_name):
        if user_name.data != current_user.user_name:
            user = User.query.filter_by(user_name=user_name.data).first()
            if user:
                raise ValidationError('That username is not available, please select a different username.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('An account already exists by this email, Please login.')

class searchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
    submit = SubmitField('Search')

class blogForm(FlaskForm):
    blog_title = StringField('blog_title',validators=[DataRequired()])
    blog_body = TextAreaField('blog_body', validators=[DataRequired()])
    submit = SubmitField('Post')

class editblogForm(FlaskForm):
    blog_title = StringField('blog_title',validators=[DataRequired()])
    blog_body = TextAreaField('blog_body', validators=[DataRequired()])
    submit = SubmitField('Edit')

class followForm(FlaskForm):
    submit = SubmitField('Follow')
