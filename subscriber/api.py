from .models import Subscriber
from rest_framework import viewsets, permissions
from .serializers import SubscriberSerializer

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset= Subscriber.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = SubscriberSerializer
