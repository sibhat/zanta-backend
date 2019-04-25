from django.contrib import admin
from .models import *


# @register(User)
class UserAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(UserAdmin, self).__init__(model, admin_site)


class ClientAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(ClientAdmin, self).__init__(model, admin_site)


class ServicesAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'type']


class InvitationAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'type', 'url', 'user']


class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'user', 'question']


class AnswerAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'question_id', 'answer']


admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Services, ServicesAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
