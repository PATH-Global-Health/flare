from rest_framework import viewsets, permissions
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Survey, SurveyResult
from .serializers import SurveySerializer, SurveyResultSerializer

class SurveyViewSet(viewsets.ModelViewSet):
    queryset= Survey.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = SurveySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    parser_classes = (MultiPartParser,FormParser,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class SurveyResultViewSet(viewsets.ModelViewSet):
    queryset= SurveyResult.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = SurveyResultSerializer
    search_fields = ['phone_number', 'session_id']

    # can be accessed using /results/?survey_id=2
    def list(self, request, *args, **kwargs):
        survey_id = self.request.query_params.get("survey_id", None)
        if survey_id is None:       
            queryset = SurveyResult.objects.all()     
        else:                                  
            queryset = SurveyResult.objects.filter(survey_id=survey_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
    