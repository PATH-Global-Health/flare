from .models import Subscriber
from rest_framework import viewsets, permissions
from .serializers import SubscriberSerializer

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset= Subscriber.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = SubscriberSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
