# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import sys
sys.path.insert(0, 'C:\\Users\\feder\\chatbot')

import os, django
os.environ["DJANGO_SETTINGS_MODULE"] = 'chatbot.settings'
django.setup()
from chatbot.models import Portfolio, Profile, Newspost, Balance, InvestedBalance

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Count
from random import randint
from django.db.models import Sum
from decimal import Decimal
import random


class GiveFollowingAdvice(Action):
    def name(self) -> Text:
        return "action_give_following_advice"

    def run(self, dispatcher, tracker, domain):
        not_followed_portfolios = Portfolio.objects.filter(followed=False)

        highest_changing_portfolio_name = None

        if not not_followed_portfolios:
            message = "You are following everyone at the moment."
        else:
            highest_change = 10
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
            else:
                message = "I don't think there is anyone you should start following right now."

        dispatcher.utter_message(message)

        return [SlotSet("name", highest_changing_portfolio_name)]


class GiveUnfollowingAdvice(Action):
    def name(self) -> Text:
        return "action_give_unfollowing_advice"

    def run(self, dispatcher, tracker, domain):
        followed_portfolios = Portfolio.objects.filter(followed=True)

        lowest_changing_portfolio_name = None

        if not followed_portfolios:
            message = "You are following everyone at the moment."
        else:
            lowest_change = 0
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
            else:
                message = "I don't think there is anyone you should stop following right now."

        dispatcher.utter_message(message)

        return [SlotSet("name", lowest_changing_portfolio_name)]


class FetchPortfolio(Action):
    def name(self) -> Text:
        return "action_fetch_portfolio"

    def run(self, dispatcher, tracker, domain):
        profile_name = tracker.get_slot('name')

        amount = None
        amount_query = None

        if profile_name is None:
            portfolio_query = "invalid"
        else:
            portfolio_query = None

            for e in tracker.latest_message['entities']:
                print('E vvvvvvvvvvvvvvvvvvvvv')
                print(e)

                if e['entity'] == 'CARDINAL':
                    try:
                        amount = round(Decimal(e['value']), 2)
                        print('AMOUNT vvvvvvvvvv')
                        print(amount)
                    except IndexError:
                        amount_query = 'invalid'
                        print('INVALID AMOUNT')

            try:
                profile_object = Profile.objects.get(name__icontains=profile_name)
                profile_name = profile_object.name

                portfolio = Portfolio.objects.get(profile=profile_object.id)

                if portfolio.followed:
                    portfolio_query = "followed"
                else:
                    portfolio_query = "not_followed"

                if amount is not None and amount > 0:
                    amount_query = "valid"
                elif amount is not None and amount <= 0:
                    amount_query = "invalid"

            except IndexError:
                print("PORTFOLIO INDEX ERROR")
                portfolio_query = "invalid"

        print("returning slots")

        return [SlotSet("portfolio_query", portfolio_query), SlotSet("name", profile_name), SlotSet("amount_query", amount_query), SlotSet("amount", amount)]


class AskFollowAmount(Action):
    def name(self) -> Text:
        return "action_ask_follow_amount"

    def run(self, dispatcher, tracker, domain):
        profile_name = tracker.get_slot('name')

        message = "How much would you like to invest?"

        dispatcher.utter_message(message)

        return [SlotSet("name", profile_name)]


class Follow(Action):
    def name(self) -> Text:
        return "action_follow"

    def run(self, dispatcher, tracker, domain):
        profile_name = tracker.get_slot('name')

        if profile_name is None:
            message = "Sorry, I can't find that portfolio. Have you spelt the name correctly?"
        else:
            print('NAME vvvvvvvvvvvvv')
            print(profile_name)

            profile_object = Profile.objects.get(name__icontains=profile_name)
            portfolio = Portfolio.objects.get(profile=profile_object.id)

            amount_query = tracker.get_slot('amount_query')
            amount = tracker.get_slot('amount')

            if amount is None:
                print('AMOUNT SLOT IS EMPTY')

                try:
                    print('TRYING TO SET AMOUNT FROM ENTITY')
                    amount = round(Decimal(tracker.latest_message['entities'][0]['value']), 2)
                    if amount > 0:
                        print('AMOUNT ENTITY IS VALID')
                        amount_query = 'valid'
                    else:
                        print('AMOUNT ENTITY IS INVALID')
                        amount_query = 'invalid'
                except IndexError:
                    amount_query = 'invalid'
            else:
                amount_query = 'valid'

            print('AMOUNT vvvvvvvvvvvvv')

            if amount_query == 'valid':
                balance = Balance.objects.first()
                balance.amount -= round(Decimal(amount), 2)

                if balance.amount < 0:
                    message = "I'm afraid your current balance is not sufficient."
                else:
                    balance.save()

                    portfolio.followed = True
                    portfolio.invested = round(Decimal(amount), 2)
                    portfolio.save()
                    print(Portfolio.objects.filter(followed=True).aggregate(Sum('invested')).get('invested__sum'))
                    message = "You are now following " + profile_name.title() + "."
            else:
                message = "That's not a valid amount."

        dispatcher.utter_message(message)

        return[]


class Unfollow(Action):
    def name(self) -> Text:
        return "action_unfollow"

    def run(self, dispatcher, tracker, domain):
        profile_name = tracker.get_slot('name')

        message = ''

        if profile_name is None:
            message = "Sorry, I can't find that portfolio. Have you spelt the name correctly?"
        else:
            profile_object = Profile.objects.get(name__icontains=profile_name)
            portfolio = Portfolio.objects.get(profile=profile_object.id)

            balance = Balance.objects.first()
            balance.amount += portfolio.invested
            balance.save()

            portfolio.followed = False
            portfolio.invested = 0.00
            portfolio.save()

            message = "You have stopped following " + profile_name.title() + "."

        dispatcher.utter_message(message)

        return[]


class AddAmount(Action):
    def name(self) -> Text:
        return "action_add_amount"

    def run(self, dispatcher, tracker, domain):
        profile_name = tracker.get_slot('name')

        profile_object = Profile.objects.get(name__icontains=profile_name)
        portfolio = Portfolio.objects.get(profile=profile_object.id)

        amount = tracker.get_slot('amount')

        if amount is None:
            try:
                amount = tracker.latest_message['entities'][0]['value']

            except IndexError:
                message = "That's not a valid amount."

        if amount is not None:
            amount = round(Decimal(amount), 2)

            if amount > 0:
                balance = Balance.objects.first()
                balance.amount -= amount

                if balance.amount < 0:
                    message = "I'm afraid your current balance is not sufficient."
                else:
                    balance.save()

                    portfolio.invested += amount
                    portfolio.save()

                    message = "You have invested another £" + str(amount) + " in " + profile_name.title() + "."
            else:
                message = "That's not a valid amount."
        else:
            message = "That's not a valid amount."

        dispatcher.utter_message(message)

        return []


class WithdrawAmount(Action):
    def name(self):
        return "action_withdraw_amount"

    def run(self, dispatcher, tracker, domain):
        profile_name = tracker.get_slot('name')

        profile_object = Profile.objects.get(name__icontains=profile_name)
        portfolio = Portfolio.objects.get(profile=profile_object.id)

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
                balance = Balance.objects.first()
                balance.amount += amount
                balance.save()

                if portfolio.invested == 0:
                    portfolio.followed = False
                    message = "You have stopped following " + profile_name.title() + "."
                else:
                    message = "You have withdrawn £" + str(amount) + " from " + profile_name.title() + "."

                portfolio.save()
        else:
            message = "That's not a valid amount."

        dispatcher.utter_message(message)

        return []


class UnfollowEveryone(Action):
    def name(self):
        return "action_unfollow_everyone"

    def run(self, dispatcher, tracker, domain):

        followed_portfolios = Portfolio.objects.filter(followed=True)

        if not followed_portfolios:
            message = "You are not following anyone."
        else:
            balance = Balance.objects.first()

            for portfolio in followed_portfolios:
                balance.amount += portfolio.invested

                portfolio.followed = False
                portfolio.invested = 0.00

                portfolio.save()

            balance.save()

            message = "You have unfollowed everyone."

        dispatcher.utter_message(message)

        return []


class ShouldIFollowAdvice(Action):
    def name(self):
        return 'action_should_i_follow_advice'

    def run(self, dispatcher, tracker, domain):
        message = ''

        profile_name = tracker.get_slot('name')

        if profile_name is None:
            message = "Sorry, I can't find that portfolio. Have you spelt the name correctly?"
        else:
            profile_object = Profile.objects.get(name__icontains=profile_name)
            portfolio = Portfolio.objects.get(profile=profile_object.id)

            chatbot_change = round(portfolio.chatbotNextChange)

            answer = ''
            increase_or_decrease = ''

            if chatbot_change >= 30:
                answer = 'Definitely!'
                increase_or_decrease = 'increase by ' + str(abs(chatbot_change)) + '%'
            elif chatbot_change >= 10:
                answer = 'Yes.'
                increase_or_decrease = 'increase by ' + str(abs(chatbot_change)) + '%'
            elif chatbot_change > 0:
                answer = 'Up to you.'
                increase_or_decrease = 'only increase by ' + str(abs(chatbot_change)) + '%'
            elif chatbot_change == 0:
                answer = 'Not really.'
                increase_or_decrease = 'not change'
            elif chatbot_change > -10:
                answer = 'Not really.'
                increase_or_decrease = 'decrease by ' + str(abs(chatbot_change)) + '%'
            elif chatbot_change > -30:
                answer = 'No.'
                increase_or_decrease = 'decrease by ' + str(abs(chatbot_change)) + '%'
            else:
                answer = 'Definitely not!'
                increase_or_decrease = 'decrease by ' + str(abs(chatbot_change)) + '%'

            message = answer + ' I believe ' + profile_name.title() + '\'s portfolio will ' + increase_or_decrease + ' next month.'

        dispatcher.utter_message(message)

        return[]


class ShouldIUnfollowAdvice(Action):
    def name(self):
        return 'action_should_i_unfollow_advice'

    def run(self, dispatcher, tracker, domain):
        message = ''

        profile_name = tracker.get_slot('name')

        if profile_name is None:
            message = "Sorry, I can't find that portfolio. Have you spelt the name correctly?"
        else:
            profile_object = Profile.objects.get(name__icontains=profile_name)
            portfolio = Portfolio.objects.get(profile=profile_object.id)

            chatbot_change = round(portfolio.chatbotNextChange)

            answer = ''
            increase_or_decrease = ''

            if chatbot_change >= 30:
                answer = 'Definitely not!'
                increase_or_decrease = 'increase by ' + str(abs(chatbot_change)) + '%'
            elif chatbot_change >= 10:
                answer = 'No.'
                increase_or_decrease = 'increase by ' + str(abs(chatbot_change)) + '%'
            elif chatbot_change > 0:
                answer = 'Not really.'
                increase_or_decrease = 'only increase by ' + str(abs(chatbot_change)) + '%'
            elif chatbot_change == 0:
                answer = 'Up to you.'
                increase_or_decrease = 'not change'
            elif chatbot_change > -10:
                answer = 'Yes.'
                increase_or_decrease = 'decrease by ' + str(abs(chatbot_change)) + '%'
            elif chatbot_change > -30:
                answer = 'Yes.'
                increase_or_decrease = 'decrease by ' + str(abs(chatbot_change)) + '%'
            else:
                answer = 'Definitely!'
                increase_or_decrease = 'decrease by ' + str(abs(chatbot_change)) + '%'

            message = answer + ' I believe ' + profile_name.title() + '\'s portfolio will ' + increase_or_decrease + ' next month.'

        dispatcher.utter_message(message)

        return[]


class ResetSlots(Action):
    def name(self):
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("portfolio_query", None), SlotSet("name", None), SlotSet("amount_query", None), SlotSet("amount", None)]
