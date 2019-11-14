How to run the code

1) Make sure to create database
  Go on terminal and type: python 
  >> from app import db 
  >>db.create_all()
  
3) Make sure to install all necessary packages
  a) Can check which one is missing via requirements.txt
  b)pip install [NAME]
  
 4)If there is any trouble, please post on Git.
 
 
Features(All of Verification found in app.py)
1) Sign Up
  Asks user to register their username, email, and password via class RegistrationForm(FlaskForm) in app.py. It will save the data in an sqlite file named 'db.sqlite'. 
2) Login
  Asks user for username and password. If both the username and password match the data in 'user' table in db.sqlite, then it will allow the user to enter dashboard.html. If else, it will flash a message, "Invalid username/password" and will not let the user through.
3) Logout
  Once logged in, in the upper navigation bar of the website, there is a icon called 'Log out'. Once clicked, will exit user from /dashboard and go back to index. Will have to log in again in order to go back to /dashboard
4) Forgot Password
  Link is located in Login page. Once in, calls "reset_request" method and asks user for email. If email matches the database,
  a token link(which expires in 30 minutes) will be sent to the respected email wiht the message, "SJSU Nigerian Prince in Dire Need".        Upon clicking on the link, the user will be sent to /reset_password/<token> where he/she can create a new password to replace the previous one.
5) Share
  This feature gives the logged in user options to share the URL via social media sites such as LinkedIn, Facebook, Twitter, and Google+.
6) To Do List
    User can input a short text and once submitted, can be seen as a bulletin point on the dashboard page and adds the data into the 'todo' table. It is also possible to remove by just clicking on the button to the right named, "Completed". This will remove the selected text and bullet points below it will move up.
7) Add Events
    User can set a time, event, and an alarm. Located in addevents.html.
8) Google Calendar API
    Once logged in, will be able to see Google Calendar and be able to edit if logged in to "danieltran150@gmail.com". There is a issue where it will only show one user(the one who implemented it) because the API will not work otherwise and implementing oAuth2 was too difficult considering the time constraint and complexity to complete it . 
  
