from django.urls import path
from rest_framework import routers
from .views import SurveyViewSet, SurveyResultViewSet, GatewayView

router = routers.DefaultRouter()
router.register('api/surveys', SurveyViewSet, 'surveys')
router.register('api/results', SurveyResultViewSet, 'results')

urlpatterns = [
    path(r'api/gateway/', GatewayView.as_view(), name='gateway')
]

urlpatterns += router.urls
