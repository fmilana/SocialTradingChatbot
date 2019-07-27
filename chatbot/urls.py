# coding: utf-8
from django.contrib import admin
from django.urls import path, include

from .views import (
    welcome_page,
    chatbot_page,
    update_portfolios,
    update_balances,
    get_next_changes,
    participants_view,
    )

urlpatterns = [
    path('', welcome_page, name='welcome'),
    path('chatbot/', chatbot_page, name='chatbot'),
    path('imagetagging/', include('imagetagging.urls'), name='imagetagging'),
    path('updateportfolios/', update_portfolios, name='updateportfolios'),
    path('updatebalances/', update_balances, name='updatebalances'),
    path('getnextchanges/', get_next_changes, name='getnextchanges'),
    path('participants/', participants_view, name='participants-view'),

]
