from django.contrib import admin

from .models import State, County, SimulationRun

admin.site.register(State)

class CountyAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'hospital_bed_capacity', 'icu_bed_capacity', 'ventilator_capacity')
    list_editable = ('hospital_bed_capacity', 'icu_bed_capacity', 'ventilator_capacity')
    search_fields = ['name', 'state__name']

admin.site.register(County, CountyAdmin)

admin.site.register(SimulationRun)

