from rest_framework import generics, permissions
from django.db.models import Max
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer

class ReportView(generics.RetrieveAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    
    def get(self, request, format=None):
        max_record = self.get_queryset().aggregate(r=Max('pk')).get('r')
        report = Report.objects.get(id = max_record)

        serializer = ReportSerializer(report)
        return Response(serializer.data)
