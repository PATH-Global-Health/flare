from .models import Subscriber
from rest_framework import viewsets, permissions
from .serializers import SubscriberSerializer

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset= Subscriber.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = SubscriberSerializer
