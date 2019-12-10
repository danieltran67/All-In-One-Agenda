from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from myapp.models import User, db


class LoginForm(FlaskForm):
    """
        A form for entering username and password.
        Takes strings and verifies the data in the current database.
         """
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    """
        Requires a string that is at 4-15 characters long.
    """
    password = PasswordField('Password', validators=[InputRequired()])
    """
        Requires a string.
    """
    remember = BooleanField('Remember me')
    """
        Remembers the user next time they attempt to log in.
    """
    submit = SubmitField('Log In')
    """
        Submit checks if the username and password is valid in the database. If so, the site will take user to
        the dashboard ( via def dashboard() in routes.py).
    """


class RegisterForm(FlaskForm):
    """
        A form to register your email, username, and password.
        Takes the input(e.g, email) and outputs it to the database. If email is already taken, then
        it will print an error message.
    """

    email = StringField('Email', validators=[InputRequired(), Email(message="Choose a valid email"), Length(max=50)])
    """
        Requires a string that is at 1-50 characters long.
    """
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    """
        Requires a string that is at 4-15 characters long.
    """
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])
    """
        Requires a string that is at 4-80 characters long.
    """
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Choose a different email.')


class RequestResetForm(FlaskForm):
    """
        A form that asks for a valid email.
        This page opens when you click the link "Forgot Password" located in the login page.
        If valid, sends the email via yagmail a token link. The token characters are randomly generated and expires in
        30 minutes due to the functions in models.py.
        If invalid, print invalid message and prevents code from sending a request token.
    """
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    """
        A form that changes the password.
        Link can only be accessed by having a non-expired token link.
        User enters a new string (password) and submits. The new password then replaces
        the old password in the database.

    """
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=40)])
    """
        Requires a string that is at 4-40 characters long.
    """
    submit = SubmitField('Reset Password')
    """
        Submits the input as the new password.
    """
