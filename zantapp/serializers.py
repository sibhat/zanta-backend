from rest_framework import serializers
from django.contrib.auth.models import Group

from .models import User, Profile, Client, Guest, Services, Invitation


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ("url", "photo", "headline", "summary")


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ("url", "partner_one_first_name", "partner_one_last_name",
                  "partner_two_first_name", "partner_two_last_name")


class GuestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Guest
        fields = ("url","email", "friend_of")


class ServicesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Services
        fields = ("url", "type")


class InvitationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Invitation
        fields = ("url", "type", "user")

