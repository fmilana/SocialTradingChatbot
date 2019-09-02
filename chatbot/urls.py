# coding: utf-8
from django.urls import path, include

from .views import (
    welcome_page,
    information_page,
    consent_page,
    instructions_page,
    chatbot_page,
    get_condition_active,
    update_portfolios,
    update_balances,
    update_month,
    update_results,
    get_next_changes,
    participants_view,
    store_bot_message,
    results_page,
    questionnaire_view,
    get_portfolios_view,
    get_profiles_view,
    get_balance_view,
    follow_unfollow_portfolio,
    add_withdraw_amount,
    increase_fallback_count,
    create_user_action
    )

urlpatterns = [
    path('', welcome_page, name='welcome'),
    path('information/', information_page, name='information'),
    path('consent/', consent_page, name='consent'),
    path('instructions/', instructions_page, name='instructions'),
    path('investment/', chatbot_page, name='chatbot'),
    path('imagetagging/', include('imagetagging.urls'), name='imagetagging'),
    path('getconditionactive/', get_condition_active, name='getconditionactive'),
    path('updateportfolios/', update_portfolios, name='updateportfolios'),
    path('updatebalances/', update_balances, name='updatebalances'),
    path('updatemonth/', update_month, name='updatemonth'),
    path('updateresults/', update_results, name='updateresults'),
    path('getnextchanges/', get_next_changes, name='getnextchanges'),
    path('participants/', participants_view, name='participants-view'),
    path('storebotmessage/', store_bot_message, name='storebotmessage'),
    path('results/', results_page, name='resultspage'),
    path('questionnaire/', questionnaire_view, name='questionnaire_view'),
    path('getportfolios/', get_portfolios_view, name='getportfoliosview'),
    path('getprofiles/', get_profiles_view, name='getprofiles'),
    path('getbalance/', get_balance_view, name='getbalance'),
    path('followunfollowportfolio/', follow_unfollow_portfolio, name='followunfollowportfolio'),
    path('addwithdrawamount/', add_withdraw_amount, name='addwithdrawamount'),
    path('increasefallbackcount/', increase_fallback_count, name='increasefallbackcount'),
    path('createuseraction/', create_user_action, name='createuseraction')
]
