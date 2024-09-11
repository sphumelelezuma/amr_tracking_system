from django import forms
from .models import Post
from django.contrib.auth.models import User
from .models import Post, UserProfile  # Ensure UserProfile is imported correctly
from .models import ResistanceData
from .models import Location, Pathogen

class ResistanceDataForm(forms.ModelForm):
    class Meta:
        model = ResistanceData
        fields = ['pathogen', 'resistance_percentage', 'location', 'date_collected']
        widgets = {
            'date_collected': forms.SelectDateWidget()  # Optional, for better date picking UX
        }
    location = forms.ModelChoiceField(queryset=Location.objects.all(), empty_label="Select Location")
    pathogen = forms.ModelChoiceField(queryset=Pathogen.objects.all(), empty_label="Select Pathogen")
    
class PathogenForm(forms.ModelForm):
    class Meta:
        model = Pathogen
        fields = ['name']  # Assuming Pathogen model has a 'name' field

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']  # Assuming Location model has a 'name' field

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'document']  # Fields to include in the form
