
rm ./db.sqlite3
rm ./dashboard/migrations/0001_initial.py
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata ./fixtures/classes.yaml
python manage.py loaddata ./fixtures/slots.yaml
python manage.py loaddata ./fixtures/dungeons.yaml
python manage.py loaddata ./fixtures/karazhan_bosses.yaml
python manage.py loaddata ./fixtures/karazhan_items.yaml
env DJANGO_SUPERUSER_PASSWORD=admin DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_EMAIL=admin@home.local ./manage.py createsuperuser --noinput
python manage.py runserver
#echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
