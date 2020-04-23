from .models import Language
from rest_framework import viewsets, permissions
from .serializers import LanguageSerializer

class LanguageViewSet(viewsets.ModelViewSet):
    
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset= Language.objects.all()
    serializer_class = LanguageSerializer
