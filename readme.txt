IS212 G10 T6 Git Repository Link:
https://github.com/gailteh/IS212-T6-LJPS

INSTALLATION GUIDE
(1) set up and run a WAMP or MAMP server

(2) execute the contents of 'db.sql' in phpMyAdmin, i.e. at:

       http://localhost/phpmyadmin  OR
	   http://localhost/phpMyAdmin

(3) find your web server's root directory (e.g. C:\wamp\www) copy the folder IS212-T6-LJPS into there

(4) if you don't already have Flask installed, do:

	   python -m pip install flask
	   python -m pip install flask_cors
	   python -m pip install Flask-SQLAlchemy
	   python -m pip install mysql-connector-python

(5) in the 'backend' directory, run: 
    python role_skill_course.py

(6) open another terminal. in the 'backend' directory, run: 
    python lj.py

(7) go to http://localhost/IS212-T6-LJPS/frontend/ where the application should be working!