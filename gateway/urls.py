from django.urls import path
from . import views

urlpatterns = [
    path(r'',views.GatewayView.as_view(), name='gateway')
]
