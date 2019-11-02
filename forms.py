from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, InputRequired, Length, Email


class LoginForm(FlaskForm):  # this will have different form fields

    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])  # Username is the label on HTML
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):  # this will have different form fields
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=15)])  # Username is the label on HTML
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=80)])
    submit = SubmitField('Sign Up')
