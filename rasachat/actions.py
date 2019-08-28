# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, UserUtteranceReverted

import sys, os
#sys.path.insert(0, 'C:\\Users\\feder\\chatbot')
here = os.path.dirname(__file__)
project_dir, _ = os.path.split(here)
#print('project_dir', project_dir)
sys.path.insert(0, project_dir)

import os, django
os.environ["DJANGO_SETTINGS_MODULE"] = 'investment_bot.settings'
django.setup()
from chatbot.models import Portfolio, Profile, Balance, Month, UserAction, FallbackCount
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Count
from django.core.exceptions import MultipleObjectsReturned
from random import randint
from django.db.models import Sum
from decimal import Decimal, InvalidOperation
import random


class WhatICanDo(Action):
    def name(self) -> Text:
        return "action_what_I_can_do"

    def run(self, dispatcher, tracker, domain):

        dispatcher.utter_template("utter_what_i_can_do", tracker)

        return []


class GiveGeneralAdvice(Action):
    def name(self) -> Text:
        return "action_give_general_advice"

    def run(self, dispatcher, tracker, domain):
        # print(tracker.current_state())
        username = tracker.current_state()["sender_id"]

        user = User.objects.get(username=username)

        highest_change = 1
        highest_pronoun = ''
        lowest_change = -1
        lowest_pronoun = ''

        highest_changing_portfolio_name = None
        lowest_changing_portfolio_name = None

        for portfolio in Portfolio.objects.filter(user=user):

            chatbot_change = portfolio.chatbotNextChange

            if portfolio.followed and chatbot_change < lowest_change:
                lowest_change = chatbot_change
                lowest_changing_portfolio_name = portfolio.profile.name

                if portfolio.profile.gender == 'Male':
                    lowest_pronoun = 'his'
                else:
                    lowest_pronoun = 'her'

            elif not portfolio.followed and chatbot_change > highest_change:
                highest_change = chatbot_change
                highest_changing_portfolio_name = portfolio.profile.name

                if portfolio.profile.gender == 'Male':
                    highest_pronoun = 'his'
                else:
                    highest_pronoun = 'her'

        message = ''
        profile_name = None

        portfolio_query = None

        higher_is_greater = highest_change >= abs(lowest_change)

        buttons = []

        if highest_changing_portfolio_name is None and lowest_changing_portfolio_name is None:
            message = "You're doing great! I don't think you should follow or unfollow anyone else this month."
            buttons.append({"title": "Give me some advice", "payload": "Give me some advice"})
            if Portfolio.objects.filter(user=user, followed=False):
                buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
            if Portfolio.objects.filter(user=user, followed=True):
                buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})
        elif lowest_changing_portfolio_name is None or higher_is_greater:
            message = "I think you should start following " + highest_changing_portfolio_name + ". I believe " + highest_pronoun + " porfolio will increase by " + str(round(highest_change)) + "% next month."
            profile_name = highest_changing_portfolio_name
            portfolio_query = "not_followed"
            buttons.append({"title": "Do it", "payload": "Do it"})
            buttons.append({"title": "Never mind", "payload": "Never mind"})
        else:
            message = "I think you should stop following " + lowest_changing_portfolio_name + ". I believe " + lowest_pronoun + " porfolio will decrease by " + str(round(abs(lowest_change))) + "% next month."
            profile_name = lowest_changing_portfolio_name
            portfolio_query = "followed"
            buttons.append({"title": "Do it", "payload": "Do it"})
            buttons.append({"title": "Never mind", "payload": "Never mind"})

        # dispatcher.utter_message(message)

        dispatcher.utter_button_message(message, buttons)

        return [SlotSet("name", profile_name), SlotSet("portfolio_query", portfolio_query)]


class GiveFollowingAdvice(Action):
    def name(self) -> Text:
        return "action_give_following_advice"

    def run(self, dispatcher, tracker, domain):
        username = tracker.current_state()["sender_id"]

        user = User.objects.get(username=username)

        not_followed_portfolios = Portfolio.objects.filter(user=user, followed=False)

        highest_changing_portfolio_name = None

        buttons = []

        if not not_followed_portfolios:
            message = "You are following everyone at the moment."
        else:
            highest_change = 1
            pronoun = ''

            for portfolio in not_followed_portfolios:
                chatbot_change = portfolio.chatbotNextChange

                if chatbot_change > highest_change:
                    highest_change = chatbot_change
                    highest_changing_portfolio_name = portfolio.profile.name

                    if portfolio.profile.gender == 'Male':
                        pronoun = 'his'
                    else:
                        pronoun = 'her'

            if highest_changing_portfolio_name is not None:
                message = "I think you should start following " + highest_changing_portfolio_name + ". I believe " + pronoun + " porfolio will increase by " + str(round(abs(highest_change))) + "% next month."
                buttons.append({"title": "Do it", "payload": "Do it"})
                buttons.append({"title": "Never mind", "payload": "Never mind"})
            else:
                message = "I don't think there is anyone you should start following right now."
                buttons.append({"title": "Give me some advice", "payload": "Give me some advice"})
                if Portfolio.objects.filter(user=user, followed=False):
                    buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
                if Portfolio.objects.filter(user=user, followed=True):
                    buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})

        dispatcher.utter_button_message(message, buttons)

        return [SlotSet("name", highest_changing_portfolio_name)]


class GiveUnfollowingAdvice(Action):
    def name(self) -> Text:
        return "action_give_unfollowing_advice"

    def run(self, dispatcher, tracker, domain):
        username = tracker.current_state()["sender_id"]

        user = User.objects.get(username=username)

        followed_portfolios = Portfolio.objects.filter(user=user, followed=True)

        lowest_changing_portfolio_name = None

        buttons = []

        if not followed_portfolios:
            message = "You are not following anyone at the moment."
            buttons.append({"title": "Give me some advice", "payload": "Give me some advice"})
            if Portfolio.objects.filter(user=user, followed=False):
                buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
            if Portfolio.objects.filter(user=user, followed=True):
                buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})
        else:
            lowest_change = -1
            pronoun = ''

            for portfolio in followed_portfolios:
                chatbot_change = portfolio.chatbotNextChange

                if chatbot_change < lowest_change:
                    lowest_change = chatbot_change
                    lowest_changing_portfolio_name = portfolio.profile.name

                    if portfolio.profile.gender == 'Male':
                        pronoun = 'his'
                    else:
                        pronoun = 'her'

            if lowest_changing_portfolio_name is not None:
                message = "I think you should stop following " + lowest_changing_portfolio_name + ". I believe " + pronoun + " porfolio will decrease by " + str(round(abs(lowest_change))) + "% next month."
                buttons.append({"title": "Do it", "payload": "Do it"})
                buttons.append({"title": "Never mind", "payload": "Never mind"})
            else:
                message = "I don't think there is anyone you should stop following right now."
                buttons.append({"title": "Give me some advice", "payload": "Give me some advice"})
                if Portfolio.objects.filter(user=user, followed=False):
                    buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
                if Portfolio.objects.filter(user=user, followed=True):
                    buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})

        dispatcher.utter_button_message(message, buttons)

        return [SlotSet("name", lowest_changing_portfolio_name)]


class FetchPortfolio(Action):
    def name(self) -> Text:
        return "action_fetch_portfolio"

    def run(self, dispatcher, tracker, domain):
        username = tracker.current_state()["sender_id"]

        user = User.objects.get(username=username)

        # profile_name = tracker.get_slot('name')

        profile_name = ''
        for e in tracker.latest_message['entities']:
            if e['entity'] == 'name':
                profile_name = e['value']

        amount = None
        amount_query = None

        if profile_name is None:
            portfolio_query = "invalid"
        else:
            portfolio_query = None

            for e in tracker.latest_message['entities']:

                if e['entity'] == 'CARDINAL':
                    try:
                        amount = round(Decimal(e['value']), 2)
                    except (IndexError, InvalidOperation):
                        amount_query = 'invalid'

            try:
                profile_object = Profile.objects.get(name__icontains=profile_name)
                profile_name = profile_object.name

                portfolio = Portfolio.objects.get(user=user, profile=profile_object.id)

                if portfolio.followed:
                    portfolio_query = "followed"
                else:
                    portfolio_query = "not_followed"

                if amount is not None and amount > 0:
                    amount_query = "valid"
                elif amount is not None and amount <= 0:
                    amount_query = "invalid"

            except (IndexError, MultipleObjectsReturned):
                portfolio_query = "invalid"

        print("returning slots")

        return [SlotSet("portfolio_query", portfolio_query), SlotSet("name", profile_name), SlotSet("amount_query", amount_query), SlotSet("amount", amount)]


class AskAddAmount(Action):
    def name(self) -> Text:
        return "action_ask_add_amount"

    def run(self, dispatcher, tracker, domain):
        user = User.objects.get(username=(tracker.current_state())["sender_id"])

        profile_name = tracker.get_slot('name')

        balance = Balance.objects.get(user=user)
        available_amount = balance.available

        message = "How much would you like to invest?"

        buttons = []
        tenPercent = int(50 * round(float(available_amount/10)/50))
        twentyPercent = tenPercent*2
        fourtyPercent = twentyPercent*2

        if tenPercent > 0:
            buttons.append({"title": "£" + str(tenPercent), "payload": "£" + str(tenPercent)})
        if twentyPercent > 0 and twentyPercent != tenPercent:
            buttons.append({"title": "£" + str(twentyPercent), "payload": "£" + str(twentyPercent)})
        if fourtyPercent > 0 and fourtyPercent != twentyPercent:
            buttons.append({"title": "£" + str(fourtyPercent), "payload": "£" + str(fourtyPercent)})

        # dispatcher.utter_button_message(message)

        dispatcher.utter_button_message(message, buttons)

        return [SlotSet("name", profile_name)]


class AskWithdrawAmount(Action):
    def name(self) -> Text:
        return "action_ask_withdraw_amount"

    def run(self, dispatcher, tracker, domain):

        user = User.objects.get(username=(tracker.current_state())["sender_id"])

        profile_name = tracker.get_slot('name')

        profile_object = Profile.objects.get(name__icontains=profile_name)
        portfolio = Portfolio.objects.get(user=user, profile=profile_object.id)

        buttons = []
        tenPercent = int(10 * round(float(portfolio.invested/10)/10))
        twentyPercent = tenPercent*2
        fiftyPercent = tenPercent*5

        if tenPercent > 0:
            buttons.append({"title": "£" + str(tenPercent), "payload": "£" + str(tenPercent)})
        if twentyPercent > 0 and twentyPercent != tenPercent:
            buttons.append({"title": "£" + str(twentyPercent), "payload": "£" + str(twentyPercent)})
        if fiftyPercent > 0 and fiftyPercent != twentyPercent:
            buttons.append({"title": "£" + str(fiftyPercent), "payload": "£" + str(fiftyPercent)})

        message = "How much would you like to withdraw?"

        dispatcher.utter_button_message(message, buttons)

        return [SlotSet("name", profile_name)]


class Follow(Action):
    def name(self) -> Text:
        return "action_follow"

    def run(self, dispatcher, tracker, domain):
        username = tracker.current_state()["sender_id"]

        user = User.objects.get(username=username)

        print(user.username)

        profile_name = tracker.get_slot('name')

        if profile_name is None:
            message = "Sorry, I can't find that portfolio. Have you spelt the name correctly?"
        else:
            profile_object = Profile.objects.get(name__icontains=profile_name)
            portfolio = Portfolio.objects.get(user=user, profile=profile_object.id)

            amount_query = tracker.get_slot('amount_query')
            amount = tracker.get_slot('amount')

            if amount is None:
                try:
                    amount = round(Decimal(tracker.latest_message['entities'][0]['value']), 2)
                    if amount > 0:
                        amount_query = 'valid'
                    else:
                        amount_query = 'invalid'
                except IndexError:
                    amount_query = 'invalid'
            else:
                amount_query = 'valid'

            if amount_query == 'valid':
                balance = Balance.objects.get(user=user)
                available_before = balance.available
                invested_before = balance.invested
                balance.available -= round(Decimal(amount), 2)

                if balance.available < 0:
                    message = "I'm afraid your current balance is not sufficient."
                else:
                    balance.save()

                    portfolio.followed = True
                    portfolio.invested = round(Decimal(amount), 2)
                    portfolio.save()
                    print(Portfolio.objects.filter(followed=True).aggregate(Sum('invested')).get('invested__sum'))
                    message = "You are now following " + profile_name.title() + "."

                    month = Month.objects.get(user=user).number

                    user_action = UserAction(user=user,
                     month=month,
                     available=available_before,
                     invested=invested_before,
                     portfolio=profile_name.title(),
                     chatbot_change=portfolio.chatbotNextChange,
                     newspost_change=portfolio.newspostNextChange,
                     action="Follow",
                     amount=amount)
                    user_action.save()
            else:
                message = "That's not a valid amount."

        buttons = []

        buttons.append({"title": "Give me some advice", "payload": "Give me some advice"})
        if Portfolio.objects.filter(user=user, followed=False):
            buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
        if Portfolio.objects.filter(user=user, followed=True):
            buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})

        dispatcher.utter_button_message(message, buttons)

        return[]


class Unfollow(Action):
    def name(self) -> Text:
        return "action_unfollow"

    def run(self, dispatcher, tracker, domain):
        user = User.objects.get(username=(tracker.current_state())["sender_id"])

        profile_name = tracker.get_slot('name')

        message = ''

        if profile_name is None:
            message = "Sorry, I can't find that portfolio. Have you spelt the name correctly?"
        else:
            profile_object = Profile.objects.get(name__icontains=profile_name)
            portfolio = Portfolio.objects.get(user=user, profile=profile_object.id)

            balance = Balance.objects.get(user=user)
            available_before = balance.available
            invested_before = balance.invested
            portfolio_invested_before = portfolio.invested
            balance.available += portfolio.invested
            balance.save()

            portfolio.followed = False
            portfolio.invested = 0.00
            portfolio.save()

            month = Month.objects.get(user=user).number

            user_action = UserAction(user=user,
             month=month,
             available=available_before,
             invested=invested_before,
             portfolio=profile_name.title(),
             chatbot_change=portfolio.chatbotNextChange,
             newspost_change=portfolio.newspostNextChange,
             action="Unfollow",
             amount=portfolio_invested_before)
            user_action.save()

            message = "You have stopped following " + profile_name.title() + "."

        buttons = []

        buttons.append({"title": "Give me some advice", "payload": "Give me some advice"})
        if Portfolio.objects.filter(user=user, followed=False):
            buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
        if Portfolio.objects.filter(user=user, followed=True):
            buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})

        dispatcher.utter_button_message(message, buttons)

        return[]


class AddAmount(Action):
    def name(self) -> Text:
        return "action_add_amount"

    def run(self, dispatcher, tracker, domain):
        user = User.objects.get(username=(tracker.current_state())["sender_id"])

        profile_name = tracker.get_slot('name')

        message = ''
        buttons = []

        if profile_name is None:
            message = "Sorry, I can't find that portfolio. Have you spelt the name correctly?"
        else:
            profile_object = Profile.objects.get(name__icontains=profile_name)
            portfolio = Portfolio.objects.get(user=user, profile=profile_object.id)

            amount = tracker.get_slot('amount')

            if amount is None:
                try:
                    amount = tracker.latest_message['entities'][0]['value']

                except IndexError:
                    message = "That's not a valid amount."

            if amount is not None:
                amount = round(Decimal(amount), 2)

                if amount > 0:
                    balance = Balance.objects.get(user=user)
                    available_before = balance.available
                    invested_before = balance.invested
                    balance.available -= amount

                    if balance.available < 0:
                        message = "I'm afraid your current balance is not sufficient."
                    else:
                        balance.save()

                        portfolio.invested += amount
                        portfolio.save()

                        month = Month.objects.get(user=user).number

                        user_action = UserAction(user=user,
                         month=month,
                         available=available_before,
                         invested=invested_before,
                         portfolio=profile_name.title(),
                         chatbot_change=portfolio.chatbotNextChange,
                         newspost_change=portfolio.newspostNextChange,
                         action="Add",
                         amount=amount)
                        user_action.save()

                        message = "You have invested another £" + str(amount) + " in " + profile_name.title() + "."
                else:
                    message = "That's not a valid amount."
            else:
                message = "That's not a valid amount."

        buttons.append({"title": "Give me some advice", "payload": "Give me some advice"})
        if Portfolio.objects.filter(user=user, followed=False):
            buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
        if Portfolio.objects.filter(user=user, followed=True):
            buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})

        dispatcher.utter_button_message(message, buttons)

        return []


class WithdrawAmount(Action):
    def name(self):
        return "action_withdraw_amount"

    def run(self, dispatcher, tracker, domain):
        username = tracker.current_state()["sender_id"]

        user = User.objects.get(username=username)

        profile_name = tracker.get_slot('name')

        message = ''
        buttons = []

        if profile_name is None:
            message = "Sorry, I can't find that portfolio. Have you spelt the name correctly?"
        else:
            profile_object = Profile.objects.get(name__icontains=profile_name)
            portfolio = Portfolio.objects.get(user=user, profile=profile_object.id)

            amount = tracker.get_slot('amount')

            if amount is None:
                try:
                    amount = tracker.latest_message['entities'][0]['value']

                except IndexError:
                    message = "That's not a valid amount."

            if amount is not None:
                amount = round(Decimal(amount), 2)

                portfolio.invested -= amount

                if portfolio.invested < 0:
                    message = "That's not a valid amount to withdraw."
                else:
                    balance = Balance.objects.get(user=user)
                    available_before = balance.available
                    invested_before = balance.invested
                    balance.available += amount
                    balance.save()

                    if portfolio.invested == 0:
                        portfolio.followed = False
                        message = "You have stopped following " + profile_name.title() + "."
                    else:
                        message = "You have withdrawn £" + str(amount) + " from " + profile_name.title() + "."

                    portfolio.save()

                    month = Month.objects.get(user=user).number

                    user_action = UserAction(user=user,
                     month=month,
                     available=available_before,
                     invested=invested_before,
                     portfolio=profile_name.title(),
                     chatbot_change=portfolio.chatbotNextChange,
                     newspost_change=portfolio.newspostNextChange,
                     action="Withdraw",
                     amount=amount)
                    user_action.save()
            else:
                message = "That's not a valid amount."

        buttons.append({"title": "Give me some advice", "payload": "Give me some advice"})
        if Portfolio.objects.filter(user=user, followed=False):
            buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
        if Portfolio.objects.filter(user=user, followed=True):
            buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})

        dispatcher.utter_button_message(message, buttons)

        return []


class UnfollowEveryone(Action):
    def name(self):
        return "action_unfollow_everyone"

    def run(self, dispatcher, tracker, domain):
        username = tracker.current_state()["sender_id"]

        user = User.objects.get(username=username)

        followed_portfolios = Portfolio.objects.filter(user=user, followed=True)

        if not followed_portfolios:
            message = "You are not following anyone."
        else:
            balance = Balance.objects.get(user=user)

            for portfolio in followed_portfolios:
                available_before = balance.available
                invested_before = balance.invested
                portfolio_invested_before = portfolio.invested
                balance.available += portfolio.invested

                portfolio.followed = False
                portfolio.invested = 0.00

                portfolio.save()

                month = Month.objects.get(user=user).number

                user_action = UserAction(user=user,
                 month=month,
                 available=available_before,
                 invested=invested_before,
                 portfolio=portfolio.profile.name.title(),
                 chatbot_change=portfolio.chatbotNextChange,
                 newspost_change=portfolio.newspostNextChange,
                 action="Unfollow",
                 amount=portfolio_invested_before)
                user_action.save()

            balance.save()

            message = "You have unfollowed everyone."

        buttons = []

        buttons.append({"title": "Give me some advice", "payload": "Give me some advice"})
        if Portfolio.objects.filter(user=user, followed=False):
            buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
        if Portfolio.objects.filter(user=user, followed=True):
            buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})

        dispatcher.utter_button_message(message, buttons)

        return []


class ShouldIFollowAdvice(Action):
    def name(self):
        return 'action_should_i_follow_advice'

    def run(self, dispatcher, tracker, domain):
        username = tracker.current_state()["sender_id"]

        user = User.objects.get(username=username)
        message = ''

        profile_name = tracker.get_slot('name')
        amount_query = tracker.get_slot('amount_query')

        buttons = []

        if profile_name is None:
            profile_name = tracker.latest_message['entities'][0]['value']

        if profile_name is None:
            message = "Sorry, I can't find that portfolio. Have you spelt the name correctly?"
            buttons.append({"title": "Give me some advice", "payload": "Give me some advice"})
            if Portfolio.objects.filter(user=user, followed=False):
                buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
            if Portfolio.objects.filter(user=user, followed=True):
                buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})
        else:
            profile_object = Profile.objects.get(name__icontains=profile_name)
            portfolio = Portfolio.objects.get(user=user, profile=profile_object.id)

            chatbot_change = round(portfolio.chatbotNextChange)

            answer = ''
            increase_or_decrease = ''

            if chatbot_change >= 30:
                answer = 'Absolutely! '
                increase_or_decrease = 'increase by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(True, user, portfolio.followed, profile_object.gender, amount_query, buttons)
            elif chatbot_change > 0:
                answer = 'Yes. '
                increase_or_decrease = 'increase by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(True, user, portfolio.followed, profile_object.gender, amount_query, buttons)
            elif chatbot_change == 0:
                answer = 'Not really. '
                increase_or_decrease = 'not change'
                self.appendButtons(False, user, portfolio.followed, profile_object.gender, amount_query, buttons)
            elif chatbot_change > -10:
                answer = 'Not really. '
                increase_or_decrease = 'decrease by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(False, user, portfolio.followed, profile_object.gender, amount_query, buttons)
            elif chatbot_change > -30:
                answer = 'No. '
                increase_or_decrease = 'decrease by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(False, user, portfolio.followed, profile_object.gender, amount_query, buttons)
            else:
                answer = 'Absolutely not! '
                increase_or_decrease = 'decrease by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(False, user, portfolio.followed, profile_object.gender, amount_query, buttons)

            message = answer + 'I believe ' + profile_name.title() + '\'s portfolio will ' + increase_or_decrease + ' next month.'

        dispatcher.utter_button_message(message, buttons)

        return[]

    def appendButtons(self, user, positive, followed, gender, amount_query, buttons):
        pronoun = ''
        if gender == "Male":
            pronoun = 'him'
        else:
            pronoun = 'her'

        if positive and followed:
            if amount_query == 'valid':
                buttons.append({"title": "Do it", "payload": "Do it"})
                buttons.append({"title": "Withdraw from " + pronoun, "payload": "Withdraw from " + pronoun})
                buttons.append({"title": "Unfollow " + pronoun, "payload": "Unfollow " + pronoun})
                buttons.append({"title": "Never mind", "payload": "Never mind"})
            else:
                buttons.append({"title": "Invest more on " + pronoun, "payload": "Invest more on " + pronoun})
                buttons.append({"title": "Withdraw from " + pronoun, "payload": "Withdraw from " + pronoun})
                buttons.append({"title": "Unfollow " + pronoun, "payload": "Unfollow " + pronoun})
                buttons.append({"title": "Never mind", "payload": "Never mind"})
        elif positive and not followed:
            if amount_query == 'valid':
                buttons.append({"title": "Do it", "payload": "Do it"})
                buttons.append({"title": "Never mind", "payload": "Never mind"})
            else:
                buttons.append({"title": "Follow " + pronoun, "payload": "Follow " + pronoun})
                buttons.append({"title": "Never mind", "payload": "Never mind"})
        elif not positive and followed:
            if amount_query == 'valid':
                buttons.append({"title": "Do it anyway", "payload": "Do it anyway"})
                buttons.append({"title": "Unfollow " + pronoun, "payload": "Unfollow " + pronoun})
                buttons.append({"title": "Withdraw from " + pronoun, "payload": "Withdraw from " + pronoun})
                buttons.append({"title": "Never mind", "payload": "Never mind"})
            else:
                buttons.append({"title": "Unfollow " + pronoun, "payload": "Unfollow " + pronoun})
                buttons.append({"title": "Withdraw from " + pronoun, "payload": "Withdraw from " + pronoun})
                buttons.append({"title": "Invest more on " + pronoun, "payload": "Invest more on " + pronoun})
                buttons.append({"title": "Never mind", "payload": "Never mind"})
        else:
            buttons.append({"title": "Do it anyway", "payload": "Do it anyway"})
            buttons.append({"title": "Give me some advice", "payload": "Give me some advice"})
            if Portfolio.objects.filter(user=user, followed=False):
                buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
            if Portfolio.objects.filter(user=user, followed=True):
                buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})


class ShouldIUnfollowAdvice(Action):
    def name(self):
        return 'action_should_i_unfollow_advice'

    def run(self, dispatcher, tracker, domain):
        username = tracker.current_state()["sender_id"]

        user = User.objects.get(username=username)

        message = ''

        profile_name = tracker.get_slot('name')
        amount_query = tracker.get_slot('amount_query')

        buttons = []

        if profile_name is None:
            profile_name = tracker.latest_message['entities'][0]['value']

        if profile_name is None:
            message = "Sorry, I can't find that portfolio. Have you spelt the name correctly?"
        else:
            profile_object = Profile.objects.get(name__icontains=profile_name)
            portfolio = Portfolio.objects.get(user=user, profile=profile_object.id)

            chatbot_change = round(portfolio.chatbotNextChange)

            answer = ''
            increase_or_decrease = ''

            if chatbot_change >= 30:
                answer = 'Absolutely not! '
                increase_or_decrease = 'increase by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(False, user, profile_object.gender, amount_query, buttons)
            elif chatbot_change > 0:
                answer = 'No.'
                increase_or_decrease = 'increase by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(False, user, profile_object.gender, amount_query, buttons)
            elif chatbot_change == 0:
                increase_or_decrease = 'not change'
                self.appendButtons(False, user, profile_object.gender, amount_query, buttons)
            elif chatbot_change > -10:
                answer = 'Yes. '
                increase_or_decrease = 'decrease by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(True, user, profile_object.gender, amount_query, buttons)
            elif chatbot_change > -30:
                answer = 'Yes. '
                increase_or_decrease = 'decrease by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(True, user, profile_object.gender, amount_query, buttons)
            else:
                answer = 'Absolutely! '
                increase_or_decrease = 'decrease by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(True, user, profile_object.gender, amount_query, buttons)

            message = answer + ' I believe ' + profile_name.title() + '\'s portfolio will ' + increase_or_decrease + ' next month.'

        dispatcher.utter_button_message(message, buttons)

        return[]

    def appendButtons(self, user, positive, gender, amount_query, buttons):
        pronoun = ''
        if gender == "Male":
            pronoun = 'him'
        else:
            pronoun = 'her'

        if positive:
            if amount_query == 'valid':
                buttons.append({"title": "Do it", "payload": "Do it"})
                buttons.append({"title": "Invest more on " + pronoun, "payload": "Invest more on " + pronoun})
                buttons.append({"title": "Never mind", "payload": "Never mind"})
            else:
                buttons.append({"title": "Invest more on " + pronoun, "payload": "Invest more on " + pronoun})
                buttons.append({"title": "Withdraw from " + pronoun, "payload": "Withdraw from " + pronoun})
                buttons.append({"title": "Unfollow " + pronoun, "payload": "Unfollow " + pronoun})
                buttons.append({"title": "Never mind", "payload": "Never mind"})
        else:
            buttons.append({"title": "Do it anyway", "payload": "Do it anyway"})
            buttons.append({"title": "Give me some advice", "payload": "Give me some advice"})
            if Portfolio.objects.filter(user=user, followed=False):
                buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
            if Portfolio.objects.filter(user=user, followed=True):
                buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})


class ResetSlots(Action):
    def name(self):
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("portfolio_query", None), SlotSet("name", None), SlotSet("amount_query", None), SlotSet("amount", None)]


class FallbackAction(Action):
    def name(self):
        return "action_fallback"

    def run(self, dispatcher, tracker, domain):
        username = tracker.current_state()["sender_id"]

        user = User.objects.get(username=username)

        fallback_count = FallbackCount.objects.get(user=user)
        fallback_count.count += 1
        fallback_count.save()

        message = "Sorry, I didn't quite catch that."

        dispatcher.utter_message(message)

        return [UserUtteranceReverted()]
