
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from zantapp.views import *
from django.views.decorators.csrf import csrf_exempt

router = DefaultRouter(trailing_slash=True)
router.register('client', ClientViewSet)
router.register("users", UserViewSet)
router.register('groups', GroupViewSet)


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),

    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path("account/client", csrf_exempt(signup_client.as_view()), name="client"),
    # path('o/token/', views.ProfileTokenView.as_view(), name="token"),
    # view sets
    path('v1/', include(router.urls)),
]
