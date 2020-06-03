from rest_framework import serializers
from .models import County, SimulationRun, HashValue


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = ['name', 'hospital_bed_capacity',
                  'icu_bed_capacity', 'ventilator_capacity']


class SimulationRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulationRun
        fields = ['id', 'timestamp', 'model_input',
                  'model_output', ]


class HashValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashValue
        fields = ['id', 'timestamp', 'hash_value', ]
