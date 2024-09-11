import csv
from django.core.management.base import BaseCommand
from amr_app.models import Location

class Command(BaseCommand):
    help = 'Import locations from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Debugging: Print row keys
                print(row.keys())  # To see available keys in each row

                # Access CSV columns
                name = row.get('Name')
                location_type = row.get('Type')
                
                # Debugging: Print values to ensure they're correct
                print(f'Name: {name}, Type: {location_type}')

                # Save to database
                Location.objects.get_or_create(
                    name=name,
                    location_type=location_type
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported locations from CSV'))
