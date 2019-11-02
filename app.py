from flask import Flask, render_template, redirect, flash, request, url_for
# from flask_bootstrap import Bootstrap
from forms import LoginForm, RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

#Bootstrap(app)
app.config['SECRET_KEY'] = 'some-key'


# Creates a table database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))


@app.route('/')
def index():
    return render_template("base.html", title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.first())
        if user:
            if form.username.data == form.password.data:
                #return redirect(url_for('addEvents.html'))
                return render_template('addevents.html', username=form.username)
        return '<h1>Invalid username or password </h1>'
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New User has been Created</h1>' \
               '<a href="login">Login</a>'
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('register.html', title='Register', form=form)


@app.route('/welcome', methods=['POST'])
def welcome():
    name = request.form['username']  # request.form username doesn't work, need another way to grab the username.
    return render_template('welcome.html', name=name)


@app.route('/addevents')
def addEvents():
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    return render_template('addevents.html', months=months)


@app.route('/settings')
def settings():
    return render_template("settings.html", title='Settings')


if __name__ == '__main__':
    app.run()
