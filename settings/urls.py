from rest_framework import routers
from .api import LanguageViewSet, ChannelViewSet

router = routers.DefaultRouter()
router.register('api/languages', LanguageViewSet, 'languages')
router.register('api/channels', ChannelViewSet, 'channels')

urlpatterns = router.urls