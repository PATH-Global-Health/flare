from django.urls import path
from rest_framework import routers
from .views import SurveyViewSet, SurveyResultViewSet, SurveyGatewayView

router = routers.DefaultRouter()
router.register('api/surveys', SurveyViewSet, 'surveys')
router.register('api/results', SurveyResultViewSet, 'results')

urlpatterns = [
    path(r'api/survey/', SurveyGatewayView.as_view(), name='survey')
]

urlpatterns += router.urls
