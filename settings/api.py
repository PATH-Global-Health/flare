from .models import Language
from rest_framework import viewsets, permissions
from .serializers import LanguageSerializer

class LanguageViewSet(viewsets.ModelViewSet):
    queryset= Language.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = LanguageSerializer
