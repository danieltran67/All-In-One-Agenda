from flask import Flask, render_template, redirect, flash
from forms import LoginForm, RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some-key'


@app.route('/')
def index():
    return render_template("base.html", title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Username and / or password is incorrect. Please try again.'
        else:
            return render_template('welcome.html')  # redirect(url_for('welcome')) maybe try to use this? still works.
    return render_template('login.html', error=error)


@app.route('/welcome', methods=['POST'])
def welcome():
    name = request.form['username']  # request.form username doesn't work, need another way to grab the username.
    return render_template('welcome.html', name=name)


@app.route('/addevents')
def addEvents():
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    return render_template('addevents.html', months=months)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)


@app.route('/settings')
def settings():
    return render_template("settings.html",title='Settings')


if __name__ == '__main__':
    app.run()
