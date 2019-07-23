# encoding: utf-8

from django.urls import path, re_path
from .views import webhook_view

urlpatterns = [
    path('', webhook_view),
]
