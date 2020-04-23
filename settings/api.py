from .models import Language
from rest_framework import viewsets, permissions
from .serializers import LanguageSerializer

class LanguageViewSet(viewsets.ModelViewSet):
    
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset= Language.objects.all()
    serializer_class = LanguageSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)