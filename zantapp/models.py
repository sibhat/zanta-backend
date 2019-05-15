import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.http import int_to_base36
from django.utils.translation import gettext_lazy as _

ID_LENGTH = 10


def id_gen() -> str:
    """Generates random string whose length is `ID_LENGTH`."""
    return int_to_base36(uuid.uuid4().int)[:ID_LENGTH]


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a user with the given email, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class BaseModel(models.Model):
    """
    Django abstract model whose primary key is a random string and has auto create and update datetime fields.
    This acts as the base model for all other models.
    """
    id = models.CharField(max_length=ID_LENGTH, primary_key=True, default=id_gen, editable=False)
    created_at = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(verbose_name=_('updated time'), auto_now=True, db_index=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(_('email address'), max_length=255, blank=False, unique=True)  # Singular Field Uniqueness
    is_photographer = models.BooleanField(_('photographer'), default=False)
    is_client = models.BooleanField(_('client'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f'{self.email} {self.first_name} {self.last_name}'


class Profile(BaseModel):
    """Profile """

    user = models.OneToOneField(verbose_name=_('user'), to='User', related_name='%(class)s', on_delete=models.CASCADE)
    photo = models.URLField(max_length=500, blank=True)
    Story = models.CharField(_('Story'), max_length=500, blank=True)
    headline = models.CharField(_('headline'), max_length=500, blank=True)
    confirm_spending = models.BooleanField(default=False)
    # User balance
    credits = models.IntegerField(default=0)

    class Meta:
        abstract = True

    # Magic Method for a nicer representation for the profile
    def __str__(self):
        return f'{self.id}: {self.__class__.__name__}: {self.user.email}'


class SkillsField(ArrayField):
    """ArrayField subclass to be used for saving skills under Client. Requires Postgres database."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('base_field', models.CharField(max_length=30, blank=False))
        kwargs.setdefault('blank', True)
        kwargs.setdefault('default', list)
        super().__init__(*args, **kwargs)


class Client(Profile):
    """Client comment started """
    # guests = SkillsField()  # Use Guest
    partner_one_first_name = models.CharField(max_length=100)
    partner_one_last_name = models.CharField(max_length=100)
    partner_one_gender = models.CharField(max_length=50, choices=(("m", "male"), ("f", "female"),))

    partner_two_first_name = models.CharField(max_length=100)
    partner_two_last_name = models.CharField(max_length=100)
    partner_two_gender = models.CharField(max_length=50, choices=(("m", "male"), ("f", "female"),))

    wedding_date = models.DateField(verbose_name=_('wedding date'), blank=True, auto_now_add=True, db_index=True)
    reception_location = models.CharField(max_length=5000, blank=True)
    message = models.CharField(max_length=1000)
    free_apps = models.IntegerField(default=5)


class Guest(models.Model):
    user = models.ForeignKey('Client', verbose_name=_('Client id'), on_delete=models.CASCADE)
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    friend_of = models.CharField(max_length=50, choices=(("groom", "bride"),))


class Services(models.Model):
    type = models.CharField(max_length=50, choices=(("1", "Wedding"), (2, "Baptism"), (3, "Event"),))


class Invitation(models.Model):
    user = models.ForeignKey('Client', verbose_name=_('Client id'), on_delete=models.CASCADE)
    type = models.ForeignKey('Services', verbose_name=_('Invitation Type'), on_delete=models.CASCADE)
    url = models.URLField(max_length=200, blank=True)


class Question(models.Model):
    question = models.CharField(_("Question"), max_length=200, blank=True)
    user = models.ForeignKey('Client', on_delete=models.CASCADE)


class Answer(models.Model):
    answer = models.CharField(_("Answer"), max_length=200, blank=True)
    question_id = models.OneToOneField(verbose_name=_('Question Id'), to='Question',
                                       related_name='%(class)s', on_delete=models.CASCADE)


class Photographer(Profile):
    company_name = models.CharField(_('company name'), max_length=100, blank=True)
    # Get one free call per day(employer version of app / match) [pending]
    free_calls = models.IntegerField(default=0)
    postings = models.IntegerField(default=1)

