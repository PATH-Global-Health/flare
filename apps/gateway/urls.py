from django.urls import path
from .views import GatewayCovid19View

urlpatterns = [
    path(r'api/gateway/covid19', GatewayCovid19View.as_view(), name='gateway_covid19')
]
