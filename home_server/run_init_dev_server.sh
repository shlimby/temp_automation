python3 init.py dev

# Migrate DB
python3 manage.py makemigrations app
python3 manage.py migrate

# Create superuser for DB => Email does not need to be entered
python3 manage.py createsuperuser

# Start Devserver
python manage.py runserver 8080