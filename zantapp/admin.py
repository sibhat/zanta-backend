from django.contrib import admin
from .models import *


# @register(User)
class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'email']


class ClientAdmin(admin.ModelAdmin):
    readonly_fields = ['partner_one_first_name', 'partner_one_last_name']


class ServicesAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'type']


class InvitationAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'type', 'url', 'user']


class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'user', 'question']


class AnswerAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'question_id', 'answer']


admin.site.register(User, AuthorAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Services, ServicesAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
