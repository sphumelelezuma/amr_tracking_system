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
            reader = csv.DictReader(file, delimiter=';')

            # Print headers to confirm if they are correctly read
            headers = reader.fieldnames
            print(f"CSV Headers: {headers}")

            for row in reader:
                # If the keys are combined, split them manually
                if 'Name;Type' in row:
                    name_type = row['Name;Type'].split(';')  # Manually split the combined key
                    name = name_type[0].strip()
                    location_type = name_type[1].strip() if len(name_type) > 1 else ''
                else:
                    # Access CSV columns
                    name = row.get('Name', '').strip()
                    location_type = row.get('Type', '').strip()

                # Debugging: Check for missing values
                if not name:
                    self.stdout.write(self.style.ERROR(f'Missing name in row: {row}'))
                    continue  # Skip this row
                
                # Debugging: Print values to ensure they're correct
                print(f'Name: {name}, Type: {location_type}')

                # Save to database
                Location.objects.get_or_create(
                    name=name,
                    type=location_type
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported locations from CSV'))
