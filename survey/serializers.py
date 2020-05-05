from rest_framework import serializers
from .models import Survey, SurveyResult

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ('id','title', 'journeys')#'__all__' #we need to see all the fields in language model
        
class SurveyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResult
        fields = ('__all__',)