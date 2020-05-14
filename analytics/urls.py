from rest_framework import routers
from .api import ReportView

router = routers.DefaultRouter()
router.register('api/report', ReportView, 'report')

urlpatterns = router.urls