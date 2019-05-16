from datetime import timedelta

from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.models import Application, AccessToken, RefreshToken
from oauthlib import common
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from oauth2_provider.settings import oauth2_settings
from zantapp.serializers import *


@swagger_auto_schema(methods=['get'],
                     responses={200: openapi.Response('Client or Photographer profile', ClientSerializer)})
@api_view(http_method_names=['GET'])
def me(request):
    """Returns representation of the authenticated user profile (Client or Photographer) making the request."""

    if request.user.is_client:
        serializer = ClientSerializer(instance=request.user.client, context={'request': request})
    else:
        pass
        # serializer = PhotographerSerializer(instance=request.user.photographer)

    return Response(data=serializer.data)


@swagger_auto_schema(methods=['post'], request_body=ClientSerializer)
@api_view(http_method_names=['POST'])
@permission_classes([])
@transaction.atomic
def signup_client(request):

    serializer = SignupClientSerializer(data=request.data, context={'request': request})
    serializer.is_valid()
    # print("serializer error: ", serializer.errors)
    if serializer.errors:
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer.save()
        application = Application.objects.get(client_id=serializer.initial_data["client_id"])
        expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        activated_user = User.objects.get(email=serializer.data["email"])
        access_token = AccessToken(
            user=activated_user,
            scope='',
            expires=expires,
            token=common.generate_token(),
            application=application
        )
        access_token.save()
        refresh_token = RefreshToken(
            user=activated_user,
            token=common.generate_token(),
            application=application,
            access_token=access_token
        )
        refresh_token.save()

        return Response({"expires": expires, "access_token": access_token.token,
                         "refresh_token": refresh_token.token}, status=200)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows User to be viewed or edited. to be deleted!
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """"ClientViewSet comment started"""

    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
