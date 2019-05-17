
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from zantapp.views import *
from django.views.decorators.csrf import csrf_exempt

router = DefaultRouter(trailing_slash=True)
router.register('client', ClientViewSet)
router.register("users", UserViewSet)
router.register("invitation", InvitationViewSet)
router.register("service", ServicesViewSet)


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),

    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path("register/client", csrf_exempt(signup_client), name="client"),
    path('me/', me, name='me'),
    path('', include(router.urls)),
]
