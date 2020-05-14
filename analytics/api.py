from rest_framework import generics
from django.db.models import Max
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer

class ReportView(generics.RetrieveAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def retrieve(self, request, *args, **kwargs):
        report = self.get_queryset().aggregate(Max('id'))
        return Response(self.get_serializer(instance=report))
