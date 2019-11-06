# All-In-One-Agenda
In order to run the website correctly, you must activate make sure the sqlite database (known as db.sqlite3) works


How to activate:
  1)Go to your IDE
  2)Install all the necessary packages
    a)if your missing X, go to your TERMINAL IDE 
      - In order to get into Terminal IDE, make sue you "cd" into your project folder. E.g, "cd [my location for the project folder]"
    b)Type "pip install [insert missing packages]". E.g, "pip install flask_wtf"
    c)Press Enter
  2)Open the IDE Terminal
  3)Check if db works
    a)Type "python"
    b)Type "from app import db"
    c)Type "db.create_all()"
    d)exit()
    e)Re-open a brand new terminal
    f)Type "sqlite3 db.sqlite3"
    g)Type "select * from user;"
    h)Type ".tables"
4)If it gives a text called "user" under ".tables", it works! If not, contact IT Daniel.

