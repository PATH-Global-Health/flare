import json
import yaml
from rest_framework import serializers
from ussd.core import UssdView
from .models import Survey, SurveyResult

def validate_yaml(value):
    try:
        journey = value['journeys'].read()
        journey = yaml.full_load(journey)
        is_valid, errors = UssdView.validate_ussd_journey(journey)
    except:
        raise serializers.ValidationError({"journeys":["The yaml file is invalid."]})

    if(not(is_valid)):
        raise serializers.ValidationError({"journeys":[json.dumps(errors)]})

class SurveySerializer(serializers.ModelSerializer):

    class Meta:
        model = Survey
        fields = ('id','title', 'journeys')#'__all__' #we need to see all the fields in language model
        validators = [ validate_yaml ]


def validate_result(value):
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print (value)
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    

class SurveyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResult
        fields = ('id','survey','subscriber', 'result')
        validators = [ validate_result ]