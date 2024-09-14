import csv
from django.core.management.base import BaseCommand
from amr_app.models import Pathogen

class Command(BaseCommand):
    help = 'Import pathogens from a CSV file'

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
                # Check if the row uses combined keys
                if 'Name;Description' in row:
                    # Split the combined key into name and description
                    name_description = row['Name;Description'].split(';')
                    name = name_description[0].strip()
                    description = name_description[1].strip() if len(name_description) > 1 else ''
                else:
                    # Safely retrieve the 'Name' and 'Description' columns
                    name = row.get('Name', '').strip()
                    description = row.get('Description', None)

                    # If description is None, default it to an empty string
                    if description:
                        description = description.strip()
                    else:
                        description = ''

                # Check if the name is missing, and skip the row if it is
                if not name:
                    self.stdout.write(self.style.ERROR(f'Missing name in row: {row}'))
                    continue

                # Debugging: Print name and description to verify correctness
                print(f'Name: {name}, Description: {description}')

                # Save to the database
                Pathogen.objects.get_or_create(
                    name=name,
                    defaults={'description': description}
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported pathogens from CSV'))
