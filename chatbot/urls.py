# coding: utf-8
from django.contrib import admin
from django.urls import path, include

from .views import (
    welcome_page,
    chatbot_page,
    get_condition_active,
    update_portfolios,
    update_balances,
    update_month,
    get_next_changes,
    participants_view,
    store_bot_message
    )

urlpatterns = [
    path('', welcome_page, name='welcome'),
    path('chatbot/', chatbot_page, name='chatbot'),
    path('imagetagging/', include('imagetagging.urls'), name='imagetagging'),
    path('getconditionactive/', get_condition_active, name='getconditionactive'),
    path('updateportfolios/', update_portfolios, name='updateportfolios'),
    path('updatebalances/', update_balances, name='updatebalances'),
    path('updatemonth', update_month, name='updatemonth'),
    path('getnextchanges/', get_next_changes, name='getnextchanges'),
    path('participants/', participants_view, name='participants-view'),
    path('storebotmessage/', store_bot_message, name='storebotmessage')
]
