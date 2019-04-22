from django.contrib import admin
from .models import User
# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'username']


admin.site.register(User, AuthorAdmin)