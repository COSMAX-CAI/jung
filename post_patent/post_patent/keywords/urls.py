from rest_framework import routers
from .views import KeywordsViewSet

router = routers.SimpleRouter()
router.register('', KeywordsViewSet)
#router.register(r'accounts', AccountViewSet)
urlpatterns = router.urls