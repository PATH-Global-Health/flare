from django.urls import path
from .views import Gateway

urlpatterns = [
    path(r'api/dhis/', Gateway.as_view(), name='gateway')
]
