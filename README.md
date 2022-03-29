# CSIT214 Room Booking Web Application
### Using Django (Python)
This web application was developed as part of a group project in CSIT 214 IT Project Management module from University of Wollongong.

**This web application is not officially affiliated with the University of Wollongong!**

Developed by Le Vu Nguyen Khanh.  
This was my first attempt at using Django so the structuring of the project was a bit messed up.  
You can try the web application using my personally hosted website: https://214.khanhc.me/ or on HerokuApp at https://csit214.herokuapp.com/.  

- Root account (has ALL permissions including account management):
Username: root
Password: admin


- Superuser account (has permission to launch/reject rooms and view room usage, cannot create or edit rooms, can view but not edit bookings, cannot view or edit promo codes, cannot manage accounts):
Username: admin
Password: asdfasdf123


- Staff accounts (can create and edit rooms, cannot change room’s launch status, can view but not edit bookings, can view and edit promo codes, cannot manage accounts):
Username: staff1
Password: asdfasdf123
Username: staff2
Password: asdfasdf123


- Student account:
Username: student
Password: asdfasdf123

---
# Instructions
Clone the repo, setup a python virtual environment and install the packages in requirements.txt (`pip3 install -r requirements.txt`), then run `python manage.py runserver`. You can also open the folder with VSCode and set the python interpreter to the appropriate virtual environment then press F5 to start the web app more easily.

The application is setup to use SQLite locally but Postgres when run on Heroku (it made sense back then), so gitignore has the .env file so that when we commit local changes, the production server (in my case Heroku) does not get the .env file and start using SQLite too. The .env file is forcily included in this repo. You can change this behavior by modifying the gettingstarted/settings.py file to change the database used or remove the .env file if you do not want to use SQLite locally.
