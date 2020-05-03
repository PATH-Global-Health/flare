from rest_framework import serializers
from .models import Language, Channel, Configuration
from message.serializers import MessageStatusSerializer

class LanguageSerializer(serializers.ModelSerializer):

    # messages = MessageSerializer(many=True, read_only=True)
    messages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Language
        fields = ('id', 'name', 'code', 'messages')#'__all__' #we need to see all the fields in language model
        extra_kwargs = {'messages': {'required': False}}

class ChannelSerializer(serializers.ModelSerializer):

    # messages = MessageSerializer(many=True, read_only=True)
    messages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Channel
        fields = ('id', 'name', 'messages')
        extra_kwargs = {'messages': {'required': False}}

class ConfigurationSerializer(serializers.ModelSerializer):

    #message_detail = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    status_detail = MessageStatusSerializer(many=True, read_only=True)

    class Meta:
        model = Configuration
        fields = ('__all__')
        extra_kwargs = {'status_detail': {'required': False}}