from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = (
            'total_messages', 
            'total_subscribers', 
            'total_surveys', 
            'total_suspects', 
            'suspects_by_region', 
            'suspects_by_sex', 
            'suspects_by_age', 
            'created_at'
            )
