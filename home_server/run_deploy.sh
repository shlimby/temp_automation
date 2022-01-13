python3 init.py deploy

# Migrate DB
python3 manage.py makemigrations temp_app
python3 manage.py migrate

# Create superuser for DB => Email does not need to be entered
python3 manage.py createsuperuser
python3 manage.py collectstatic

# Deploy Django App
# Install apache server with wsgi package
sudo apt install apache2 libapache2-mod-wsgi-py3 -y

# Change permissions
sudo usermod -a -G www-data pi
sudo chown -R -f www-data:www-data /var/www/html

# Change default configuration of Apache and enable it
sudo cp django_wsgi.conf /etc/apache2/sites-available/django_wsgi.conf
sudo a2ensite django_wsgi.conf
sudo a2dissite 000-default.conf

# restart server
sudo systemctl restart apache2