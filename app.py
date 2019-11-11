from flask import render_template, request, redirect, url_for, flash, Flask
from flask_login import current_user, login_required, login_user, logout_user
from flask import Flask
from flask_wtf import FlaskForm
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


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message="Choose a valid email"), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Choose a different email.')


# Class needed for resets password page
class RequestResetForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=40)])
    submit = SubmitField('Reset Password')


@app.login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    Todolist = db.relationship('Todo', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<user: {self.username}>'

    # Creates a id token that expires in 30 minutes
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    # Takes a token, tries to load the token and returns a user id
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Todo(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     text =  db.Column(db.String(200))
     complete = db.Column(db.Boolean)
     user_id =  db.Column(db.Integer, db.ForeignKey('user.id'))

     def __repr__(self):
         return f'<post: {self.text}>'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if form.password.data == user.password:
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
        flash('Incorrect username/password. Try again.')
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = form.password.data
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('An email has been sent to reset your password')
            return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    body = f"I need $10K to save my country. I promise to handsomely " \
           f"reward you for your valiant efforts! Also here's the reset Link:" \
           f"{url_for('reset_token', token=token, _external=True)}"
    receiver = user.email
    yag.send(to=receiver,
             subject="SJSU Nigerian Prince in Dire Need",
             contents=body)


# Required for reset_request to match user
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:  # If the token is wrong or expired
        flash('That is an invalid  or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = form.password.data
        user.password = hashed_password
        db.session.commit()
        flash('Your password updated!')
        return redirect(url_for('index'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('dashboard'))

@app.route('/complete/<id>')
def complete(id):

    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()
    
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    todos = Todo.query.filter_by(complete=False).all()

    return render_template('dashboard.html', name=current_user.username, todos = todos)


@app.route('/addevents')
@login_required
def addevents():
    return render_template('addevents.html', name=current_user.username)


@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
