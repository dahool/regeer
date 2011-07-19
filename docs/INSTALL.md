Prerequisites
==============

* Python 2.5+
* Django 1.3.x
* Rcon Module requires B3 bot

Quick Install
==============

* Copy the _regeer_ folder to the desired location
* Rename settings/60-local.pyconf.example to settings/60-local.pyconf and edit with your database settings (KEEP the name 'default' on it). The database must already exists and the users needs full privileges.
* Change to the _regeer_ directory and run python manage.py syncdb to initialize the database. Follow the steps to create the super user.
* Run python manage.py initdb to initialize the application data.

The Development Server
=======================

To test your application in a local environment, run python manage.py runserver to start dev server and point a browser to http://127.0.0.1:8000/

The first time you run the application, you'll be redirected to the administrative dashboard, here you can setup the game servers.

Just go to the _Server_ tab and click in *Add* 