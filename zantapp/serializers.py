from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.models import Group
from rest_framework.validators import UniqueValidator

from .models import User, Profile, Client, Guest, Services, Invitation, Question, Photographer


class SignupClientSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', max_length=255,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(source='user.password', max_length=128, write_only=True)
    old_password = serializers.CharField(max_length=128, write_only=True, required=False)
    first_name = serializers.CharField(source='user.first_name', allow_blank=True, max_length=30, required=False)
    last_name = serializers.CharField(source='user.last_name', allow_blank=True, max_length=150, required=False)
    is_photographer = serializers.ReadOnlyField(source='user.is_photographer')
    is_client = serializers.ReadOnlyField(source='user.is_client')
    wedding_date = serializers.DateTimeField(source='client.wedding_date', required=False)

    class Meta:
        model = Client
        fields = ['email', "first_name", "password", "last_name", "old_password", "is_photographer",
                  "is_client", "wedding_date"]
        # validators = [UniqueValidator(queryset=Photographer.objects.all())]

    @transaction.atomic  # Ensure creation of both models is done
    # in a single transaction not to create inconsistencies
    def create(self, validated_data):
        """
        Creates new User and Client profile.
        """
        # Create auth user model first
        validated_user_data = validated_data.pop('user', {})
        user = User.objects.create_user(is_client=True, **validated_user_data)
        # Create Client profile
        return Client.objects.create(user=user, **validated_data)


class SignupPhotographerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', max_length=255)
    email = serializers.EmailField(source='user.email', max_length=255)
    password = serializers.CharField(source='user.password', max_length=128, write_only=True)
    old_password = serializers.CharField(max_length=128, write_only=True, required=False)
    first_name = serializers.CharField(source='user.first_name', allow_blank=True, max_length=30, required=False)
    last_name = serializers.CharField(source='user.last_name', allow_blank=True, max_length=150, required=False)
    is_photographer = serializers.ReadOnlyField(source='user.is_customer')
    is_client = serializers.ReadOnlyField(source='user.is_admin')

    class Meta:
        model = Photographer
        fields = ['email', 'username',  "first_name", "password", "last_name", "old_password", "is_photographer",
                  "is_client"]

    @transaction.atomic  # Ensure creation of both models is done
    # in a single transaction not to create inconsistencies
    def create(self, validated_data):
        """
        Creates new User and Photographer profile.
        """
        # Create auth user model first
        validated_user_data = validated_data.pop('user', {})
        user = User.objects.create_user(is_photographer=True, **validated_user_data)
        # Create Client profile
        return Photographer.objects.create(user=user, **validated_data)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """"
    UserSerializer
    """
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
    """"GuestSerializer comment started"""

    class Meta:
        model = Guest
        fields = ("url","email", "friend_of")


class ServicesSerializer(serializers.HyperlinkedModelSerializer):
    """"ServicesSerializer comment started"""

    class Meta:
        model = Services
        fields = ("url", "type")


class InvitationSerializer(serializers.HyperlinkedModelSerializer):
    """"InvitationSerializer comment started"""

    class Meta:
        model = Invitation
        fields = ("url", "type", "user")


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    """"QuestionSerializer comment started"""

    class Meta:
        model = Question
        fields = ("url", "question")

