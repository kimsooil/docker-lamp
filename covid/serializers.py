from rest_framework import serializers
from .models import County

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = ['name', 'hospital_bed_capacity', 'icu_bed_capacity', 'ventilator_capacity']