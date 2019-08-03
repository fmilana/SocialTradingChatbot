from django.contrib import admin
from import_export import resources
from import_export.admin import ExportActionModelAdmin


from .models import (
    Profile,
    Portfolio,
    Balance,
    Message,
    UserAction,
    Participant,
    Condition,
    DismissNotificationCount,
    Result,
    QuestionnaireResponse
    )

class BalanceResource(resources.ModelResource):
    class Meta:
        model = Balance
        fields = ['user', 'available', 'invested', 
                    'user_username', 'user__participant__condition_active']

class BalanceAdmin(ExportActionModelAdmin):
    list_display = ['__str__', 'available', 'invested']
    resource_class = BalanceResource


class MessageResource(resources.ModelResource):
    class Meta:
        model = Message
        fields = ['user', 'month', 'from_participant', 
                    'from_notification', 'from_button', 
                    'text', 'user_username', 'user__participant__condition_active']
        
class MessageAdmin(ExportActionModelAdmin):
    #list_display = ['participant', 'participant__user__username', 'task', 'task__task_list__name']
    #list_display = ['__str__', 'user__participant__condition_active']
    list_display = ['__str__', 'user']
    resource_class = MessageResource


class ResultResource(resources.ModelResource):
    class Meta:
        model = Result
        fields = ['month', 'profit', 'images_tagged', 'total', 
                    'user_username', 'user__participant__condition_active']

class ResultAdmin(ExportActionModelAdmin):
    #list_display = ['participant', 'participant__user__username', 'task', 'task__task_list__name']
    list_display = ['__str__', 'user']
    resource_class = ResultResource


class QuestionnaireResponseResource(resources.ModelResource):
    class Meta:
        model = QuestionnaireResponse
        fields = ['user', 'answer', 'completion_time', 'subtask_time', 
                    'created_at', 'updated_at', 
                    'user_username', 'user__participant__condition_active']

class QuestionnaireResponseAdmin(ExportActionModelAdmin):
    #list_display = ['participant', 'participant__user__username', 'task', 'task__task_list__name']
    list_display = ['__str__', 'user']
    resource_class = QuestionnaireResponseResource


class UserActionResource(resources.ModelResource):
    class Meta:
        model = UserAction
        fields = ['user', 'month', 'available', 'invested', 
                    'portfolio', 'chatbot_change', 'newspost_change', 
                    'action', 'amount',
                    'user_username', 'user__participant__condition_active']

class UserActionAdmin(ExportActionModelAdmin):
    #list_display = ['participant', 'participant__user__username', 'task', 'task__task_list__name']
    list_display = ['__str__', 'user']
    resource_class = UserActionResource


admin.site.register(Balance, BalanceAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(UserAction, UserActionAdmin)
admin.site.register(QuestionnaireResponse, QuestionnaireResponseAdmin)
admin.site.register(Profile)
admin.site.register(Portfolio)
admin.site.register(Participant)
admin.site.register(Condition)
admin.site.register(DismissNotificationCount)
