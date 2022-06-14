#from rest_framework import routers
from rest_framework_nested import routers
from .views import PatentsViewSet, SearchViewSet
from django.urls import path, include

router = routers.SimpleRouter()
router.register('', PatentsViewSet)
#router.register(r'accounts', AccountViewSet)

search_router = routers.NestedSimpleRouter(router, r'', lookup='keyword')
search_router.register(r'keyword', SearchViewSet, basename='patent-keyword')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(search_router.urls)),
]