from .models import Message
from rest_framework import viewsets, permissions
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset= Message.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
