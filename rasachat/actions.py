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
from chatbot.models import Portfolio, Profile, Balance, InvestedBalance

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Count
from random import randint
from django.db.models import Sum
from decimal import Decimal


class GiveFollowingAdvice(Action):
    def name(self) -> Text:
        return "action_give_following_advice"

    def run(self, dispatcher, tracker, domain):
        not_followed_portfolios = Portfolio.objects.filter(followed=False)

        if not not_followed_portfolios:
            message = "You are following everyone at the moment."
        else:
            count = not_followed_portfolios.aggregate(count=Count('id'))['count']

            random_index = randint(0, count-1)

            random_not_followed_portfolio = not_followed_portfolios[random_index]
            profile = random_not_followed_portfolio.profile

            message = "I think you should start following " + profile.name + "."

        dispatcher.utter_message(message)

        return []


class GiveUnfollowingAdvice(Action):
    def name(self) -> Text:
        return "action_give_unfollowing_advice"

    def run(self, dispatcher, tracker, domain):
        followed_portfolios = Portfolio.objects.filter(followed=True)

        if not followed_portfolios:
            message = "You aren't following anyone at the moment."
        else:
            count = followed_portfolios.aggregate(count=Count('id'))['count']

            random_index = randint(0, count-1)

            random_followed_portfolio = followed_portfolios[random_index]
            profile = random_followed_portfolio.profile

            message = "I think you should stop following " + profile.name + "."

        dispatcher.utter_message(message)

        return []


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
                portfolio = Portfolio.objects.get(profile=profile_object.id)

                if portfolio.followed:
                    portfolio_query = "followed"
                else:
                    portfolio_query = "not_followed"

                if amount is not None and amount > 0:
                    amount_query = "valid"

            except IndexError:
                print("PORTFOLIO INDEX ERROR")
                portfolio_query = "invalid"

        print("returning slots")

        return [SlotSet("portfolio_query", portfolio_query), SlotSet("name", profile_name), SlotSet("amount_query", amount_query), SlotSet("amount", amount)]


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
                try:
                    amount = round(Decimal(tracker.latest_message['entities'][0]['value']), 2)
                    amount_query = 'valid'
                except IndexError:
                    print('INVALID AMOUNT')
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

        amount = round(Decimal(tracker.get_slot('amount')), 2)

        balance = Balance.objects.first()
        balance.amount -= amount

        if balance.amount < 0:
            message = "I'm afraid your current balance is not sufficient."
        else:
            balance.save()

            portfolio.invested += amount
            portfolio.save()

            message = "You have invested another £" + str(amount) + " in " + profile_name.title() + "."

        dispatcher.utter_message(message)

        return []


class WithdrawAmount(Action):
    def name(self):
        return "action_withdraw_amount"

    def run(self, dispatcher, tracker, domain):
        profile_name = tracker.get_slot('name')

        profile_object = Profile.objects.get(name__icontains=profile_name)
        portfolio = Portfolio.objects.get(profile=profile_object.id)

        amount = round(Decimal(tracker.get_slot('amount')), 2)

        portfolio.invested -= amount

        if portfolio.invested < 0:
            message = "That's not a valid amount to withdraw."#
        else:
            if portfolio.invested == 0:
                portfolio.followed = False

            portfolio.save()

            balance = Balance.objects.first()
            balance.amount += amount
            balance.save()

            message = "You have withdrawn £" + str(amount) + " from " + profile_name.title() + "."

        dispatcher.utter_message(message)

        return []


class ResetSlots(Action):
    def name(self):
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("portfolio_query", None), SlotSet("name", None), SlotSet("amount_query", None), SlotSet("amount", None)]
