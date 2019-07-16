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
        profile_name = tracker.latest_message['entities'][0]['value']

        print('NAMEEEEEEEEEEEEEEEEEEEEEEEEEE')
        print(profile_name)

        try:
            profile_object = Profile.objects.get(name__icontains=profile_name)
            portfolio = Portfolio.objects.get(profile=profile_object.id)

            if portfolio.followed:
                return [SlotSet("portfolio_query", "followed"), SlotSet("name", profile_name)]
            else:
                return [SlotSet("portfolio_query", "not_followed"), SlotSet("name", profile_name)]

        except IndexError:
            return [SlotSet("portfolio_query", "invalid")]


class Follow(Action):
    def name(self) -> Text:
        return "action_follow"

    def run(self, dispatcher, tracker, domain):
        profile_name = tracker.get_slot('name')

        print('NAME vvvvvvvvvvvvv')
        print(profile_name)

        profile_object = Profile.objects.get(name__icontains=profile_name)
        portfolio = Portfolio.objects.get(profile=profile_object.id)

        try:
            print('AMOUNT vvvvvvvvvvvvv')
            print(tracker.latest_message['entities'][0]['value'])

            amount = round(Decimal(tracker.latest_message['entities'][0]['value']), 2)

            if amount > 0:
                balance = Balance.objects.first()
                balance.amount -= amount
                balance.save()

                portfolio.followed = True
                portfolio.invested = amount
                portfolio.save()
                print(Portfolio.objects.filter(followed=True).aggregate(Sum('invested')).get('invested__sum'))
                message = "You are now following " + profile_name + "."
            else:
                message = "That's not a valid amount."
        except IndexError:
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

        message = "You have stopped following " + profile_name + "."

        dispatcher.utter_message(message)

        return[]
