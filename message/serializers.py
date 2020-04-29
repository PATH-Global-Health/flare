from rest_framework import serializers
from .models import Message
from settings.serializers import LanguageSerializer

class MessageSerializer(serializers.ModelSerializer):
    languages = LanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ('__all__')
        extra_kwargs = {'languages': {'required': False}}
        
