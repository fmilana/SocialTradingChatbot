from django.contrib import admin

# Register your models here.

from .models import (
    Profile, Portfolio, Balance
    )

admin.site.register(Profile)
admin.site.register(Portfolio)
admin.site.register(Balance)
