# This script is used to initialize the database with 100 most populated locations
# Need to install django-extensions first
# "pip install django-extensions"
# To use this script: "python manage.py runscript init_db --dir-policy each"

from subscribe.models import Location


def run():
    with open('top_cities.txt') as f:
        for line in f:
            location_obj = Location(name=line.rstrip())
            location_obj.save()
            print('Added location: ' + line.rstrip())
