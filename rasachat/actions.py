# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import sys
sys.path.insert(0, 'C:\\Users\\feder\\chatbot')

import os, django
os.environ["DJANGO_SETTINGS_MODULE"] = 'chatbot.settings'
django.setup()
from chatbot.models import Portfolio

from django.db.models.aggregates import Count
from random import randint


# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message("Hello World!")
#
#         return []


class ActionGiveFollowingAdvice(Action):

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


class ActionGiveUnfollowingAdvice(Action):

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
