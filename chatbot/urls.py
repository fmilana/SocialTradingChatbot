# coding: utf-8
from django.contrib import admin
from django.urls import path, include

from .views import (
    welcome_page,
    information_page,
    consent_page,
    chatbot_page,
    get_condition_active,
    update_portfolios,
    update_balances,
    update_month,
    get_next_changes,
    participants_view,
    update_dismiss_notification_count,
    store_bot_message,
    questionnaire_view,
    )

urlpatterns = [
    path('', welcome_page, name='welcome'),
    path('information/', information_page, name='information'),
    path('consent/', consent_page, name='consent'),
    path('chatbot/', chatbot_page, name='chatbot'),
    path('imagetagging/', include('imagetagging.urls'), name='imagetagging'),
    path('getconditionactive/', get_condition_active, name='getconditionactive'),
    path('updateportfolios/', update_portfolios, name='updateportfolios'),
    path('updatebalances/', update_balances, name='updatebalances'),
    path('updatemonth', update_month, name='updatemonth'),
    path('getnextchanges/', get_next_changes, name='getnextchanges'),
    path('participants/', participants_view, name='participants-view'),
    path('updatedismissnotificationcount/', update_dismiss_notification_count, name='updatedismissnotificationcount'),
    path('storebotmessage/', store_bot_message, name='storebotmessage'),
    path('questionnaire/', questionnaire_view, name='questionnaire_view'),

]
