from django.shortcuts import render

from oauth2_provider.models import AccessToken
from oauth2_provider.views import TokenView
from rest_framework import viewsets
# Create your views here.
from zantapp.models import User
from zantapp.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileTokenView(TokenView):
    """Returns OAuth2 access and refresh tokens in addition to user profile under 'profile' key"""

    def post(self, request, *args, **kwargs):
        # Get original response from OAuth2 library
        response = super().post(request=request, *args, **kwargs)
        # Return it in case any failures
        if response.status_code != 200:
            return response

        # Decode json body to add profile based on user type
        data = json.loads(response.content)
        user = AccessToken.objects.get(token=data['access_token']).user

        # Encode json and return the modified response
        response.content = json.dumps(data)
        return response
