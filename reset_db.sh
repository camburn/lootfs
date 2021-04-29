
rm ./db.sqlite3
rm ./dashboard/migrations/0001_initial.py
./manage.py makemigrations
./manage.py migrate
./manage.py loaddata ./fixtures/classes.yaml
./manage.py loaddata ./fixtures/slots.yaml
./manage.py loaddata ./fixtures/dungeons.yaml
./manage.py loaddata ./fixtures/karazhan_bosses.yaml
./manage.py loaddata ./fixtures/karazhan_items.yaml
env DJANGO_SUPERUSER_PASSWORD=admin DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_EMAIL=admin@home.local ./manage.py createsuperuser --noinput
./manage.py runserver
#echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
