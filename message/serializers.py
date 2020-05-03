from rest_framework import serializers
from .models import Message, MessageStatus

class MessageStatusSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField(source='configuration.id')
    user_id = serializers.ReadOnlyField(source='configuration.user_id')
    name=serializers.ReadOnlyField(source='configuration.name')

    class Meta:
        model = MessageStatus
        fields = ('id','name', 'user_id', 'success_count', 'error_count', 'config_error')
        validators = []

class MessageSerializer(serializers.ModelSerializer):

    status_detail = MessageStatusSerializer(source='messagestatus_set', many=True, required=False)

    class Meta:
        model = Message
        fields = ('id', 'content','status', 'celery_id','created_at', 'languages', 'channels', 'status_detail')
        optional_fields=('status_detail',)
        extra_kwargs = {
            'languages': {'required': False}, 
            'channels': {'required': False}, 
            'status_detail':{'required':False}
            }