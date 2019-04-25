
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from zantapp.views import *

router = DefaultRouter(trailing_slash=True)
router.register('client', ClientViewSet)
router.register("users", UserViewSet)
router.register('groups', GroupViewSet)


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),

    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # path('o/token/', views.ProfileTokenView.as_view(), name="token"),
    # view sets
    path('v1/', include(router.urls)),
]
