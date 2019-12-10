How to Install
======================================================================================================================
1) Make sure to create database
  a) Go on terminal and type: python > from app import db > db.create_all()

2) Make sure to install all necessary packages
  a) Can check which one is missing via requirements.txt
  b) pip install [NAME]

3)If there is any trouble, please post on Git or check FAQ below.

**File Location of Test Cases and How to Run**
  File location is located at the base directory in master branch.
  File is named, **test_app.py**.
  Run it by going to terminal and typing the command, **pytest**
  If you only want pass/fail results and don't want to see warnings, type the command, **pytest -p no:warnings**


**FAQ**
------------------------------------------------------------------------------------------------------------------
1) I can't run the database such as db.sqlite3. I've tried to pip install sqlite3.
    Answer: You will need to install sqlite online.
            Download this zip file, then extract: https://www.sqlite.org/2019/sqlite-tools-win32-x86-3300100.zip
            After you extract it, go into the folder named, "sqlite-tools-win32-x86-3300100".
            Make sure there is a application file named, "sqlite3".
            Copy(or cut) the folder mentioned before and paste it inside you C: drive.
            Usually it will be underneath Windows folder.
             Rename the folder as "sqlite3".
            Now copy the file directory path (e,g: C:\sqlite3).
            Go to Windows Search and type, "envir" till you see "Edit the system environment variables"
            Click on the button "Environment variables".
            You should see two boxes (top one is "user variables for ___" and bottom is "system variables")
            In the System Variables, click on variable called "Path" and "edit", then press "New.
            Finally, paste the path directory mentioned above and press OK.
            Done! You can now open command prompt and test it out by typing sqlite3