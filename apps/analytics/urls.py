from django.conf.urls import url
from .api import ReportView

urlpatterns = [
    url('api/reports/', ReportView.as_view()),
]