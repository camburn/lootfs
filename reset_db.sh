
rm ./db.sqlite3
#!/bin/bash
rm ./dashboard/migrations/0001_initial.py
python manage.py makemigrations
python manage.py migrate
source load_data.sh
env DJANGO_SUPERUSER_PASSWORD=admin DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_EMAIL=admin@home.local ./manage.py createsuperuser --noinput
python manage.py runserver
#echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
