from django.contrib import admin

from .models import Pathogen, Location, ResistanceData

# Register your models here.
@admin.register(Pathogen)
class PathogenAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    search_fields = ('name', 'type')

@admin.register(ResistanceData)
class ResistanceDataAdmin(admin.ModelAdmin):
    list_display = ('pathogen', 'location', 'date_collected', 'resistance_percentage')
    list_filter = ('pathogen', 'location')
    search_fields = ('pathogen__name', 'location__name')