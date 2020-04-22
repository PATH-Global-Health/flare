from rest_framework import routers
from .api import SubscriberViewSet

router = routers.DefaultRouter()
router.register('api/subscribers', SubscriberViewSet, 'subscribers')

urlpatterns = router.urls