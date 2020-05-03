from .models import Message
from rest_framework import viewsets, permissions
from .serializers import MessageSerializer
from rest_framework import filters

class MessageViewSet(viewsets.ModelViewSet):
    queryset= Message.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content', 'status']
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(status='started')
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
