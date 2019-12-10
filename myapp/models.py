from flask_sqlalchemy import SQLAlchemy
from werkzeug.routing import ValidationError
from werkzeug.routing import ValidationError
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import keyring as keyring
import yagmail
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from myapp import app


db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
        Database for holding user's username, email, password, and ToDoList.
    """
    id = db.Column(db.Integer, primary_key=True)
    """
        Database column for ID
    """
    username = db.Column(db.String(15), unique=True)
    """
        Database column for username
    """
    email = db.Column(db.String(50), unique=True)
    """
        Database column for email
    """
    password = db.Column(db.String(80))
    """
        Database column for password
    """
    Todolist = db.relationship('Todo', backref='author', lazy='dynamic')
    """
        Database relationship between tables User and Todo
    """

    def __repr__(self):
        """

        :return: Returns username in database
        """
        return f'<user: {self.username}>'

    # Creates a id token that expires in 30 minutes
    def get_reset_token(self, expires_sec=1800):
        """
        Generates a token that expires in 30 minutes and is randomly generated.
        :param expires_sec: Expires in 30 minutes
        :return: Returns a unique token
        """
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """
        Takes a token, tries to load the token and returns a user id.
        :param token: The token
        :return: Returns a user id
        """
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Todo(db.Model):
    """
    Database table for To Do list. Contains text, user id, and boolean flag
    """
    id = db.Column(db.Integer, primary_key=True)
    """
        Database Column for ID
    """
    text = db.Column(db.String(200))
    """
        Database Column for text
    """
    complete = db.Column(db.Boolean)
    """
        Database Column for completed work
    """
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """
        Database Column for User ID
    """

    def __repr__(self):
        """

        :return: Returns text.
        """
        return f'<post: {self.text}>'
