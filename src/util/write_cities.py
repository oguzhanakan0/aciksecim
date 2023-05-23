import csv
from election.models import City
from django.conf import settings

City.objects.all().delete()

with open(str(settings.BASE_DIR)+'/iller.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    created = 0
    for row in reader:
        City.objects.create(**row)
        created += 1
    print(f"-- Write Cities: created {created} --")