# amr_app/serializers.py

from rest_framework import serializers
from .models import Pathogen, Location, ResistanceData
from django.contrib.auth.models import User

class PathogenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pathogen
        fields = ['id', 'name', 'description']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'type']

class ResistanceDataSerializer(serializers.ModelSerializer):
    pathogen = PathogenSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = ResistanceData
        fields = ['id', 'pathogen', 'resistance_percentage', 'location', 'date_collected', 'user']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
