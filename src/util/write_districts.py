import csv
from election.models import District, City
from django.conf import settings

District.objects.all().delete()
cities = City.objects.all()

with open(str(settings.BASE_DIR)+'/ilceler.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    created = 0
    for row in reader:
        city = cities.get(id=row["city_id"])
        del row["city_id"]
        District.objects.create(city=city, **row)
        created += 1
    print(f"-- Write Districts: created {created} --")