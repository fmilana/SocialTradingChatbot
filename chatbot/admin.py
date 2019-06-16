from django.contrib import admin

# Register your models here.

from .models import (
    Profile, Portfolio, Newspost, Balance, InvestedBalance, Month
    )

admin.site.register(Profile)
admin.site.register(Portfolio)
admin.site.register(Newspost)
admin.site.register(Balance)
admin.site.register(InvestedBalance)
admin.site.register(Month)
