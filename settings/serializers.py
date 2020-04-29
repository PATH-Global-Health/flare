from rest_framework import serializers
from .models import Language

class LanguageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Language
        fields = ('id', 'name', 'code', 'messages')#'__all__' #we need to see all the fields in language model
        extra_kwargs = {'messages': {'required': False}}
