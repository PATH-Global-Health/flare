from django.urls import path
from .views import GatewayView

urlpatterns = [
    path(r'', GatewayView.as_view(), name='gateway')
]
