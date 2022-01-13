# Nett to know

Activate venv from django project

```
source ../venv/bin/activate
```

0 is a shortcut for 0.0.0.0. Full docs for the development server can be found in the runserver reference.

```
python manage.py runserver 8080
```

The **migrate command** looks at the INSTALLED_APPS setting and creates any necessary database tables according to the database settings in your mysite/settings.py file and the database migrations shipped with the app (we’ll cover those later). You’ll see a message for each migration it applies. If you’re interested, run the command-line client for your database and type \dt (PostgreSQL), SHOW TABLES; (MariaDB, MySQL), .tables (SQLite), or SELECT TABLE_NAME FROM USER_TABLES; (Oracle) to display the tables Django created.

```
python manage.py migrate
```

When model changes

```
python manage.py makemigrations app
```
