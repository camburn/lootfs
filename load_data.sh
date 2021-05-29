#!/bin/bash
python manage.py loaddata ./fixtures/classes.yaml
python manage.py loaddata ./fixtures/slots.yaml
python manage.py loaddata ./fixtures/dungeons.yaml
python manage.py loaddata ./fixtures/karazhan_bosses.yaml
python manage.py loaddata ./fixtures/karazhan_items.yaml