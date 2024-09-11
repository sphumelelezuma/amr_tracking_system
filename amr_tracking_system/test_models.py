import sys
import os
import django  # Import Django

# Add the root directory of the project to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the environment variable for the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amr_tracking_system.settings')

# Initialize Django
django.setup()

from amr_app.models import Pathogen, Location, ResistanceData

# Test retrieving data
pathogens = Pathogen.objects.all()
print(pathogens)

# Test creating data
new_pathogen = Pathogen(name='Test Pathogen', description='Test Description')
new_pathogen.save()
