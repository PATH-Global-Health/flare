from .models import Survey, SurveyResult
from rest_framework import viewsets, permissions
from .serializers import SurveySerializer, SurveyResultSerializer

class SurveyViewSet(viewsets.ModelViewSet):
    queryset= Survey.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = SurveySerializer

class SurveyResultViewSet(viewsets.ModelViewSet):
    queryset= SurveyResult.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = SurveyResultSerializer