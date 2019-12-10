from flask import Flask
import yagmail
import keyring as keyring
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

yagmail.register('targonthresh@gmail.com', 'a2b2c2d2')
keyring.set_password('yagmail', 'mygmailusername', 'mygmailpassword')
yag = yagmail.SMTP("targonthresh@gmail.com")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

bootstrap = Bootstrap(app)

from myapp import routes
from myapp import models
from myapp import forms
