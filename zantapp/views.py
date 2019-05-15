# from django.shortcuts import render
# from rest_framework.decorators import  permission_classes

# from oauth2_provider.models import AccessToken
# from oauth2_provider.views import TokenView
# from django.contrib.auth.models import Group
# from django.db import DatabaseError, Error
import json
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import viewsets, status
# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import login, authenticate
from rest_framework import status, permissions
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views.mixins import OAuthLibMixin
from rest_framework.views import APIView

from zantapp.serializers import *


class signup_client(OAuthLibMixin, APIView):
    permission_classes = (permissions.AllowAny,)

    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    @transaction.atomic
    def post(self, request):

        serializer = SignupClientSerializer(data=request.data, context={'request': request})
        serializer.is_valid()
        # print("serializer error: ", serializer.errors)
        if serializer.errors:
            print("error:", serializer.errors)
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            url, headers, body, token_status = self.create_token_response(request)
            if token_status != 200:
                # raise Exception(json.loads(body).get("error_description", ""))
                return Response(json.loads(body), status=token_status)

            return Response(json.loads(body), status=token_status)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited. to be deleted!
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited. to be deleted!
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """"ClientViewSet comment started"""

    queryset = Client.objects.all()
    serializer_class = ClientSerializer

