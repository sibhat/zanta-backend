from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User, Client, Guest, Services, Invitation, Question, Photographer


class ProfileSerializer(serializers.Serializer):
    """
    Serializer to be subclassed by Client and Photographer serializers.
    It allows creating and updating profiles and their related users.
    """

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
        fields = ['email', "first_name", "password", "last_name", "old_password", "is_photographer",
                  "is_client", "wedding_date"]


class SignupClientSerializer(ProfileSerializer, serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [*ProfileSerializer.Meta.fields]

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
        return Client.objects.create(user=user, partner_one_first_name=user.first_name,
                                     partner_one_last_name=user.last_name, **validated_data)


class SignupPhotographerSerializer(ProfileSerializer, serializers.ModelSerializer):

    class Meta:
        model = Photographer
        fields = [*ProfileSerializer.Meta.fields]

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
        return Photographer.objects.create(user=user,partner_one_first_name=user.first_name,
                                           partner_one_last_name=user.last_name, **validated_data)


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


class ClientSerializer(ProfileSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ["url", "id", "partner_one_first_name", "partner_one_last_name",
                  "partner_two_first_name", "partner_two_last_name", *ProfileSerializer.Meta.fields,
                  "free_apps", "partner_one_gender", "partner_two_gender"]


class GuestSerializer(serializers.HyperlinkedModelSerializer):
    """"GuestSerializer comment started"""

    class Meta:
        model = Guest
        fields = "__all__"


class ServicesSerializer(serializers.HyperlinkedModelSerializer):
    """"ServicesSerializer comment started"""

    class Meta:
        model = Services
        fields = ["id","type"]

    def create(self, validated_data, *args, **kwargs):
        validated_user_data = validated_data.pop('user', {})
        return Services.objects.create(user=validated_user_data.user.client, **validated_data)


class InvitationSerializer(serializers.HyperlinkedModelSerializer):
    """"InvitationSerializer comment started"""

    class Meta:
        model = Invitation
        fields = "__all__"


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    """"QuestionSerializer comment started"""

    class Meta:
        model = Question
        fields = "__all__"

