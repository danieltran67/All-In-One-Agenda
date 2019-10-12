from flask import Flask, render_template, redirect, flash
from forms import LoginForm, RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some-key'


@app.route('/')
def index():
    return render_template("base.html", title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me ={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', form=form, title='Login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)


@app.route('/settings')
def settings():
    return render_template("settings.html", title='Settings')


if __name__ == '__main__':
    app.run()
