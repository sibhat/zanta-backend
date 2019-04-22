
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=True)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),

    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('o/token/', views.ProfileTokenView.as_view(), name="token"),
    # view sets
    # path('', include(router.urls)),
]
