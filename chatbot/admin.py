from django.contrib import admin

# Register your models here.

from .models import (
    Profile,
    Portfolio,
    Balance,
    Message,
    UserAction,
    Participant,
    Condition,
    DismissNotificationCount,
    Result
    )

admin.site.register(Profile)
admin.site.register(Portfolio)
admin.site.register(Balance)
admin.site.register(Message)
admin.site.register(UserAction)
admin.site.register(Participant)
admin.site.register(Condition)
admin.site.register(DismissNotificationCount)
admin.site.register(Result)
