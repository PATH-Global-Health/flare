from .models import Subscriber
from rest_framework import viewsets, permissions
from .serializers import SubscriberSerializer
from rest_framework import filters

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset= Subscriber.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = SubscriberSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['phone_number']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
