from rest_framework import routers
from .api import SurveyViewSet, SurveyResultViewSet

router = routers.DefaultRouter()
router.register('api/surveys', SurveyViewSet, 'surveys')
router.register('api/results', SurveyResultViewSet, 'results')

urlpatterns = router.urls
