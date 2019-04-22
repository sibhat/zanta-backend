from django.contrib import admin
from django.core.checks import register

from .models import User


# Register your models here.

# @register(User)
class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'username']


admin.site.register(User, AuthorAdmin)
