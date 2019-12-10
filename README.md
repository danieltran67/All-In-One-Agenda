**Travis-CI**
[![Build Status](https://travis-ci.org/danieltran67/All-In-One-Agenda.svg?branch=master)](https://travis-ci.org/danieltran67/All-In-One-Agenda)

------------------------------------------------------------------------------------------
**Features**


Log In :
   Requires a username and password. Verifies it by checking the sqlite database called User.
   If it passes, user is redirected to the dashboard page.
   Includes a link if you forgot your password.

Sign Up :
   Requests user for an email, username, and password. Stores it in database if email is not yet taken.

Reset Request :
    A form that asks for a valid email.This page opens when you click the link
    "Forgot Password" located in the login page.
    If valid, sends the email via yagmail a token link. The token characters are randomly generated and expires in
   30 minutes due to the functions in models.py.
   If invalid, print invalid message and prevents code from sending a request token.

Reset Password :
    A form that changes the password. Link can only be accessed by having a non-expired token link.
   User enters a new string (password) and submits. The new password then replaces
   the old password in the database.

Dashboard :
   Shows additional features such as Google Calendar, Add Events, etc.

Reminders :
   This is where the To Do List is located and the user can add/remove tasks.

Resource :
   Several useful links to increase productivity and a shortcut to popular sites.

Add Events :
   Adds Events to the calendar. User inputs title, time, set alarm, and decide if they want
   to share the event with another user.

