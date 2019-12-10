from myapp import app, yag
from flask import render_template, redirect, url_for, flash, Flask, request
from flask_login import current_user, login_required, login_user, logout_user
from myapp.models import db, User, Todo
from myapp.forms import LoginForm, RegisterForm, ResetPasswordForm, RequestResetForm, InputRequired


@app.route('/')
def index():
    """
    The homepage of the website. Gives a summary of the purpose of the website.
    :return: Goes to HTML file called "index.html". This is the homepage before logging in.
    """
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Goes to login page and requests for username and password.
    :return: If username and password is the same as the on in the database, redirect
    user to dashboard. Else, print invalid message.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if form.password.data == user.password:
                login_user(user, remember=form.remember.data)
                flash('You were logged in')
                return redirect(url_for('dashboard'))
        flash('Incorrect username/password. Try again.')
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Goes to registration page and requests for email, username, and password. Stores members in database.
    :return: Sends user to login page after submitting a valid username, email, password.
    Else, it will not leave the page.
    """
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
    """
    Goes to a site that requests for a valid email in order to send a token link.
    :return: Prints the message, "An email has been sent to reset your password" and sends a token link
    to the email inputted. Redirects user to login page after wards. Else, keeps them at same site.
    """
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
    """
    Sends a token link to the receiver, whom is the email the user inputted in reset_request().
    Token link is made up of randomly generate characters and expires in 30 minutes.
    The link will redirect the user to the reset password page.
    """
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
    """
    Goes to a secured site that set a new password for the corresponding email.
    User inputs a new password and once submitted, the old password is replaced and new password is in its place/
    :param token: The token link sent via email. Required in order to access the page
    :return: If token is wrong or expired, print invalid message and redirects user back to the site that requests for
    a valid email. Else, output is committed in database, a message saying "Your password updated!, and redirects user
    to homepage."
    """
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
    """
    Adds a task to the To Do List.
    :return: Refreshes reminder page and adds a task to list.
    """
    todo = Todo(text=request.form['reminder'], complete=False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('reminders'))


@app.route('/complete/<id>')
def complete(id):
    """
    Turns the a to-do reminder from the To Do List as complete.
    :param id: The database table ID
    :return: Refreshes rhe dashboard and removes the text that matches the database ID in there.
    """
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()

    return redirect(url_for('reminders'))


@app.route('/delete<id>')
def delete(id):
    """
    Deletes task in To Do list.
    :param id: The database table ID
    :return: Refreshes reminder.HTML and remove a task form the list
    """
    todelete = Todo.query.filter_by(id=int(id)).delete()
    db.session.commit()

    return redirect(url_for('reminders'))


@app.route('/dashboard')
@login_required
def dashboard():
    """
    Requires a login to access. Goes to site where there is a Google Calendar, Resources, and more features.
    :return: Redirects to dashboard URL
    """
    todos = Todo.query.filter_by(complete=False).all()

    return render_template('dashboard.html', name=current_user.username, todos=todos)


@app.route('/addevents')
@login_required
def addevents():
    """
    Sends user to HTML page called "addevents.html"
    :return: Render template to addevents.html
    """
    return render_template('addevents.html', name=current_user.username)


@app.route('/editevents')
@login_required
def editevents():
    """
    Sends user to HTML page called "editevents.html"
    :return: Render template to editevents.html
    """
    return render_template('editevents.html')


@app.route('/resources')
@login_required
def resources():
    """
    Sends user to HTML page named "resources".
    :return: Redirects user to resource page.
    """
    return render_template('resources.html')


@app.route('/logout')
@login_required
def logout():
    """
    Log user out if user is logged in.
    :return: Redirects user to index.html
    """
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))
