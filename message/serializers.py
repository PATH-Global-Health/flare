from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'content','status', 'celery_id','created_at', 'languages')
        extra_kwargs = {'languages': {'required': False}}
        
