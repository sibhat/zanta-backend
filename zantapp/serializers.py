from rest_framework import serializers
from django.contrib.auth.models import Group

from .models import User, Profile, Client, Guest, Services, Invitation, Question


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'is_staff', 'is_photographer', 'is_client']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': True},
        }

    def create(self, validated_data):
        """Creates new auth user object using UserManager."""
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        # Pop out the password and give it a default value of none if it doesnt exist
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)  # Sets the hash
        return super().update(instance, validated_data)


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
        fields = ("url", "partner_one_first_name", "partner_one_last_name", "wedding_date", "reception_location",
                  "partner_two_first_name", "partner_two_last_name",
                  "message", "free_apps", "partner_one_gender", "partner_two_gender")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, validated_data):
        """Creates new user object using Client."""
        print(validated_data)
        return Client.objects.create_user(**validated_data)


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


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ("url", "question")

