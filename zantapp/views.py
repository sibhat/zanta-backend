from django.shortcuts import render
from rest_framework.decorators import  permission_classes

from oauth2_provider.models import AccessToken
from oauth2_provider.views import TokenView
from django.contrib.auth.models import Group

from rest_framework import viewsets
# Create your views here.
from zantapp.models import *
from zantapp.serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited. to be deleted!
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

