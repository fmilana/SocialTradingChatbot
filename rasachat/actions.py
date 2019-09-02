# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Text
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, UserUtteranceReverted

import re

from decimal import Decimal, InvalidOperation

import requests
import socket


PROJECT_NAME = 'investment_bot'
PROTOCOL = 'https'
DEPLOYMENT_HOSTS = ['iot.cs.ucl.ac.uk']

hostname = socket.gethostname()

if hostname in DEPLOYMENT_HOSTS:
    ROOT_URL = '%s://%s/%s' % (PROTOCOL, hostname, PROJECT_NAME)
else:
    ROOT_URL = 'http://127.0.0.1:8000'


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
        username = tracker.current_state()["sender_id"]

        profile_request = requests.get(ROOT_URL + '/getprofiles/')
        profiles = profile_request.json()

        portfolio_request = requests.post(ROOT_URL + '/getportfolios/', data = {'username':username})
        portfolios = portfolio_request.json()

        highest_change = 1
        highest_pronoun = ''
        lowest_change = -1
        lowest_pronoun = ''

        highest_changing_portfolio_name = None
        lowest_changing_portfolio_name = None

        for portfolio in portfolios:

            chatbot_change = float(portfolio['chatbotNextChange'])

            if portfolio['followed'] and chatbot_change < lowest_change:
                lowest_change = chatbot_change

                lowest_changing_profile = None

                for profile in profiles:
                    if profile['id'] == portfolio['profile_id']:
                        lowest_changing_profile = profile

                lowest_changing_portfolio_name = lowest_changing_profile['name']

                if lowest_changing_profile['gender'] == 'Male':
                    lowest_pronoun = 'his'
                else:
                    lowest_pronoun = 'her'

            elif not portfolio['followed'] and chatbot_change > highest_change:
                highest_change = chatbot_change
                highest_changing_profile = None

                for profile in profiles:
                    if profile['id'] == portfolio['profile_id']:
                        highest_changing_profile = profile

                highest_changing_portfolio_name = highest_changing_profile['name']

                if highest_changing_profile['gender'] == 'Male':
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
            buttons.append({"title": "Who should I follow?", "payload": "Who should I follow?"})
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

        dispatcher.utter_button_message(message, buttons)

        return [SlotSet("name", profile_name), SlotSet("portfolio_query", portfolio_query)]


class GiveFollowingAdvice(Action):
    def name(self) -> Text:
        return "action_give_following_advice"

    def run(self, dispatcher, tracker, domain):
        username = tracker.current_state()["sender_id"]

        profile_request = requests.get(ROOT_URL + '/getprofiles/')
        profiles = profile_request.json()

        portfolio_request = requests.post(ROOT_URL + '/getportfolios/', data = {'username':username})
        portfolios = portfolio_request.json()
        not_followed_portfolios = [portfolio for portfolio in portfolios if portfolio['followed'] == False]

        highest_changing_portfolio_name = None

        buttons = []

        if not not_followed_portfolios:
            message = "You are following everyone at the moment."
        else:
            highest_change = 1
            pronoun = ''

            for portfolio in not_followed_portfolios:
                chatbot_change = float(portfolio['chatbotNextChange'])

                if chatbot_change > highest_change:
                    highest_change = chatbot_change
                    highest_changing_portfolio_name = None

                    for profile in profiles:
                        if profile['id'] == portfolio['profile_id']:
                            highest_changing_portfolio_name = profile['name']

                    if profile['gender'] == 'Male':
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
                buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
                buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})

        dispatcher.utter_button_message(message, buttons)

        return [SlotSet("name", highest_changing_portfolio_name)]


class GiveUnfollowingAdvice(Action):
    def name(self) -> Text:
        return "action_give_unfollowing_advice"

    def run(self, dispatcher, tracker, domain):
        username = tracker.current_state()["sender_id"]

        profile_request = requests.get(ROOT_URL + '/getprofiles/')
        profiles = profile_request.json()

        portfolio_request = requests.post(ROOT_URL + '/getportfolios/', data = {'username':username})
        portfolios = portfolio_request.json()
        followed_portfolios = [portfolio for portfolio in portfolios if portfolio['followed'] == True]

        lowest_changing_portfolio_name = None

        buttons = []

        if not followed_portfolios:
            message = "You are not following anyone at the moment."
            buttons.append({"title": "Give me some advice", "payload": "Give me some advice"})
            buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
            buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})
        else:
            lowest_change = -1
            pronoun = ''

            for portfolio in followed_portfolios:
                chatbot_change = float(portfolio['chatbotNextChange'])

                if chatbot_change < lowest_change:
                    lowest_change = chatbot_change
                    lowest_changing_portfolio_name = None

                    for profile in profiles:
                        if profile['id'] == portfolio['profile_id']:
                            lowest_changing_portfolio_name = profile['name']

                    if lowest_changing_portfolio_name['gender'] == 'Male':
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
                buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
                buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})

        dispatcher.utter_button_message(message, buttons)

        return [SlotSet("name", lowest_changing_portfolio_name)]


class FetchPortfolio(Action):
    def name(self) -> Text:
        return "action_fetch_portfolio"

    def run(self, dispatcher, tracker, domain):
        username = tracker.current_state()["sender_id"]

        profile_request = requests.get(ROOT_URL + '/getprofiles/')
        profiles = profile_request.json()

        portfolio_request = requests.post(ROOT_URL + '/getportfolios/', data = {'username':username})
        portfolios = portfolio_request.json()

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
                profile_object = None

                for profile in profiles:
                    if re.search(profile_name, profile['name'], re.IGNORECASE):
                        profile_object = profile
                        profile_name = profile['name']

                portfolio_object = None

                for portfolio in portfolios:
                    if portfolio['profile_id'] == profile_object['id']:
                        portfolio_object = portfolio

                if portfolio_object['followed']:
                    portfolio_query = "followed"
                else:
                    portfolio_query = "not_followed"

                if amount is not None and amount > 0:
                    amount_query = "valid"
                elif amount is not None and amount <= 0:
                    amount_query = "invalid"

            except (IndexError):
                portfolio_query = "invalid"

        print("returning slots")

        return [SlotSet("portfolio_query", portfolio_query), SlotSet("name", profile_name), SlotSet("amount_query", amount_query), SlotSet("amount", amount)]


class AskAddAmount(Action):
    def name(self) -> Text:
        return "action_ask_add_amount"

    def run(self, dispatcher, tracker, domain):
        username = tracker.current_state()["sender_id"]

        profile_name = tracker.get_slot('name')

        balance_request = requests.post(ROOT_URL + '/getbalance/', data = {'username':username})
        balance = balance_request.json()

        available_amount = float(balance['available'])

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

        dispatcher.utter_button_message(message, buttons)

        return [SlotSet("name", profile_name)]


class AskWithdrawAmount(Action):
    def name(self) -> Text:
        return "action_ask_withdraw_amount"

    def run(self, dispatcher, tracker, domain):
        username = tracker.current_state()["sender_id"]

        profile_name = tracker.get_slot('name')

        profile_request = requests.get(ROOT_URL + '/getprofiles/')
        profiles = profile_request.json()

        portfolio_request = requests.post(ROOT_URL + '/getportfolios/', data = {'username':username})
        portfolios = portfolio_request.json()

        profile_object = None

        for profile in profiles:
            if re.search(profile_name, profile['name'], re.IGNORECASE):
                profile_object = profile
                profile_name = profile['name']

        portfolio_object = None

        for portfolio in portfolios:
            if portfolio['profile_id'] == profile_object['id']:
                portfolio_object = portfolio

        buttons = []
        tenPercent = int(10 * round(float(float(portfolio_object['invested'])/10)/10))
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

        profile_name = tracker.get_slot('name')

        if profile_name is None:
            message = "Sorry, I can't find that portfolio. Have you spelt the name correctly?"
        else:
            profile_request = requests.get(ROOT_URL + '/getprofiles/')
            profiles = profile_request.json()

            portfolio_request = requests.post(ROOT_URL + '/getportfolios/', data = {'username':username})
            portfolios = portfolio_request.json()

            profile_object = None

            for profile in profiles:
                if re.search(profile_name, profile['name'], re.IGNORECASE):
                    profile_object = profile
                    profile_name = profile['name']

            portfolio_object = None

            for portfolio in portfolios:
                if portfolio['profile_id'] == profile_object['id']:
                    portfolio_object = portfolio

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
                balance_request = requests.post(ROOT_URL + '/getbalance/', data = {'username':username})
                balance = balance_request.json()

                available_before = float(balance['available'])
                invested_before = float(balance['invested'])

                if amount > float(balance['available']):
                    message = "I'm afraid your current balance is not sufficient."
                else:
                    requests.post(ROOT_URL + '/followunfollowportfolio/', data = {'username':username, 'name':profile_name, 'action':'Follow', 'amount':round(Decimal(amount), 2)})

                    message = "You are now following " + profile_name.title() + "."

                    requests.post(ROOT_URL + '/createuseraction/', data = {'username':username, 'available_before':available_before, 'invested_before':invested_before, 'profile_name':profile_name.title(), 'chatbot_next_change':portfolio_object['chatbotNextChange'], 'newspost_next_change':portfolio_object['newspostNextChange'], 'action':'Follow', 'amount':amount})
            else:
                message = "That's not a valid amount."

        buttons = []

        buttons.append({"title": "Give me some advice", "payload": "Give me some advice"})
        buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
        buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})

        dispatcher.utter_button_message(message, buttons)

        return[]


class Unfollow(Action):
    def name(self) -> Text:
        return "action_unfollow"

    def run(self, dispatcher, tracker, domain):
        username=(tracker.current_state())["sender_id"]

        profile_name = tracker.get_slot('name')

        message = ''

        if profile_name is None:
            message = "Sorry, I can't find that portfolio. Have you spelt the name correctly?"
        else:
            # profile_object = Profile.objects.get(name__icontains=profile_name)
            # portfolio = Portfolio.objects.get(user=user, profile=profile_object.id)

            profile_request = requests.get(ROOT_URL + '/getprofiles/')
            profiles = profile_request.json()

            portfolio_request = requests.post(ROOT_URL + '/getportfolios/', data = {'username':username})
            portfolios = portfolio_request.json()

            balance_request = requests.post(ROOT_URL + '/getbalance/', data = {'username':username})
            balance = balance_request.json()

            profile_object = None
            for profile in profiles:
                if re.search(profile_name, profile['name'], re.IGNORECASE):
                    profile_object = profile
                    profile_name = profile['name']

            portfolio_object = None
            for portfolio in portfolios:
                if portfolio['profile_id'] == profile_object['id']:
                    portfolio_object = portfolio

            amount = portfolio_object['invested']

            available_before = float(balance['available'])
            invested_before = float(balance['invested'])

            requests.post(ROOT_URL + '/followunfollowportfolio/', data = {'username':username, 'name':profile_name, 'action':'Unfollow'})

            message = "You have stopped following " + profile_name.title() + "."

            requests.post(ROOT_URL + '/createuseraction/', data = {'username':username, 'available_before':available_before, 'invested_before':invested_before, 'profile_name':profile_name.title(), 'chatbot_next_change':portfolio_object['chatbotNextChange'], 'newspost_next_change':portfolio_object['newspostNextChange'], 'action':'Unfollow', 'amount':amount})

        buttons = []

        buttons.append({"title": "Give me some advice", "payload": "Give me some advice"})
        buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
        buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})

        dispatcher.utter_button_message(message, buttons)

        return[]


class AddAmount(Action):
    def name(self) -> Text:
        return "action_add_amount"

    def run(self, dispatcher, tracker, domain):
        username=tracker.current_state()["sender_id"]

        profile_name = tracker.get_slot('name')

        message = ''
        buttons = []

        if profile_name is None:
            message = "Sorry, I can't find that portfolio. Have you spelt the name correctly?"
        else:
            profile_request = requests.get(ROOT_URL + '/getprofiles/')
            profiles = profile_request.json()

            portfolio_request = requests.post(ROOT_URL + '/getportfolios/', data = {'username':username})
            portfolios = portfolio_request.json()

            balance_request = requests.post(ROOT_URL + '/getbalance/', data = {'username':username})
            balance = balance_request.json()

            profile_object = None
            for profile in profiles:
                if re.search(profile_name, profile['name'], re.IGNORECASE):
                    profile_object = profile
                    profile_name = profile['name']

            portfolio_object = None
            for portfolio in portfolios:
                if portfolio['profile_id'] == profile_object['id']:
                    portfolio_object = portfolio

            available_before = float(balance['available'])
            invested_before = float(balance['invested'])

            amount = tracker.get_slot('amount')

            if amount is None:
                try:
                    amount = tracker.latest_message['entities'][0]['value']

                except IndexError:
                    message = "That's not a valid amount."

            if amount is not None:
                amount = round(Decimal(amount), 2)

                if amount > 0:
                    if amount > float(balance['available']):
                        message = "I'm afraid your current balance is not sufficient."
                    else:
                        requests.post(ROOT_URL + '/addwithdrawamount/', data = {'username':username, 'name':profile_name, 'action':'Add', 'amount':amount})

                        message = "You have invested another £" + str(amount) + " in " + profile_name.title() + "."

                        requests.post(ROOT_URL + '/createuseraction/', data = {'username':username, 'available_before':available_before, 'invested_before':invested_before, 'profile_name':profile_name.title(), 'chatbot_next_change':portfolio_object['chatbotNextChange'], 'newspost_next_change':portfolio_object['newspostNextChange'], 'action':'Add', 'amount':amount})
                else:
                    message = "That's not a valid amount."
            else:
                message = "That's not a valid amount."

        buttons.append({"title": "Give me some advice", "payload": "Give me some advice"})
        buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
        buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})

        dispatcher.utter_button_message(message, buttons)

        return []


class WithdrawAmount(Action):
    def name(self):
        return "action_withdraw_amount"

    def run(self, dispatcher, tracker, domain):
        username = tracker.current_state()["sender_id"]

        profile_name = tracker.get_slot('name')

        message = ''
        buttons = []

        if profile_name is None:
            message = "Sorry, I can't find that portfolio. Have you spelt the name correctly?"
        else:
            profile_request = requests.get(ROOT_URL + '/getprofiles/')
            profiles = profile_request.json()

            portfolio_request = requests.post(ROOT_URL + '/getportfolios/', data = {'username':username})
            portfolios = portfolio_request.json()

            balance_request = requests.post(ROOT_URL + '/getbalance/', data = {'username':username})
            balance = balance_request.json()

            profile_object = None
            for profile in profiles:
                if re.search(profile_name, profile['name'], re.IGNORECASE):
                    profile_object = profile
                    profile_name = profile['name']

            portfolio_object = None
            for portfolio in portfolios:
                if portfolio['profile_id'] == profile_object['id']:
                    portfolio_object = portfolio

            available_before = float(balance['available'])
            invested_before = float(balance['invested'])

            amount = tracker.get_slot('amount')

            if amount is None:
                try:
                    amount = tracker.latest_message['entities'][0]['value']

                except IndexError:
                    message = "That's not a valid amount."

            if amount is not None:
                amount = round(Decimal(amount), 2)

                if float(portfolio_object['invested']) - float(amount) < 0:
                    message = "That's not a valid amount to withdraw."
                else:
                    requests.post(ROOT_URL + '/addwithdrawamount/', data = {'username':username, 'name':profile_name, 'action':'Withdraw', 'amount':amount})

                    message = "You have withdrawn £" + str(amount) + " from " + profile_name.title() + "."

                    requests.post(ROOT_URL + '/createuseraction/', data = {'username':username, 'available_before':available_before, 'invested_before':invested_before, 'profile_name':profile_name.title(), 'chatbot_next_change':portfolio_object['chatbotNextChange'], 'newspost_next_change':portfolio_object['newspostNextChange'], 'action':'Withdraw', 'amount':amount})
            else:
                message = "That's not a valid amount."

        buttons.append({"title": "Give me some advice", "payload": "Give me some advice"})
        buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
        buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})

        dispatcher.utter_button_message(message, buttons)

        return []


class UnfollowEveryone(Action):
    def name(self):
        return "action_unfollow_everyone"

    def run(self, dispatcher, tracker, domain):
        username = tracker.current_state()["sender_id"]

        portfolio_request = requests.post(ROOT_URL + '/getportfolios/', data = {'username':username})
        portfolios = portfolio_request.json()
        followed_portfolios = [portfolio for portfolio in portfolios if portfolio['followed'] == True]

        if not followed_portfolios:
            message = "You are not following anyone."
        else:
            profile_request = requests.get(ROOT_URL + '/getprofiles/')
            profiles = profile_request.json()

            for portfolio in followed_portfolios:
                balance_request = requests.post(ROOT_URL + '/getbalance/', data = {'username':username})
                balance = balance_request.json()

                available_before = balance['available']
                invested_before = balance['invested']

                profile_name = None

                for profile in profiles:
                    if portfolio['profile_id'] == profile['id']:
                        profile_name = profile['name']

                portfolio_invested_before = portfolio['invested']

                requests.post(ROOT_URL + '/followunfollowportfolio/', data = {'username':username, 'name':profile_name, 'action':'Unfollow'})

                requests.post(ROOT_URL + '/createuseraction/', data = {'username':username, 'available_before':available_before, 'invested_before':invested_before, 'profile_name':profile_name.title(), 'chatbot_next_change':portfolio['chatbotNextChange'], 'newspost_next_change':portfolio['newspostNextChange'], 'action':'Unfollow', 'amount':portfolio_invested_before})

            message = "You have unfollowed everyone."

        buttons = []

        buttons.append({"title": "Give me some advice", "payload": "Give me some advice"})
        buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
        buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})

        dispatcher.utter_button_message(message, buttons)

        return []


class ShouldIFollowAdvice(Action):
    def name(self):
        return 'action_should_i_follow_advice'

    def run(self, dispatcher, tracker, domain):
        username = tracker.current_state()["sender_id"]

        message = ''

        profile_name = tracker.get_slot('name')
        amount_query = tracker.get_slot('amount_query')

        buttons = []

        if profile_name is None:
            profile_name = tracker.latest_message['entities'][0]['value']

        if profile_name is None:
            message = "Sorry, I can't find that portfolio. Have you spelt the name correctly?"
            buttons.append({"title": "Give me some advice", "payload": "Give me some advice"})
            buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
            buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})
        else:
            profile_request = requests.get(ROOT_URL + '/getprofiles/')
            profiles = profile_request.json()

            portfolio_request = requests.post(ROOT_URL + '/getportfolios/', data = {'username':username})
            portfolios = portfolio_request.json()

            profile_object = None
            for profile in profiles:
                if re.search(profile_name, profile['name'], re.IGNORECASE):
                    profile_object = profile
                    profile_name = profile['name']

            portfolio = None
            for p in portfolios:
                if p['profile_id'] == profile_object['id']:
                    portfolio = p

            chatbot_change = round(float(portfolio['chatbotNextChange']))

            answer = ''
            increase_or_decrease = ''

            if chatbot_change >= 30:
                answer = 'Absolutely! '
                increase_or_decrease = 'increase by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(True, portfolio['followed'], profile_object['gender'], amount_query, buttons)
            elif chatbot_change > 0:
                answer = 'Yes. '
                increase_or_decrease = 'increase by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(True, portfolio['followed'], profile_object['gender'], amount_query, buttons)
            elif chatbot_change == 0:
                answer = 'Not really. '
                increase_or_decrease = 'not change'
                self.appendButtons(False, portfolio['followed'], profile_object['gender'], amount_query, buttons)
            elif chatbot_change > -10:
                answer = 'Not really. '
                increase_or_decrease = 'decrease by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(False, portfolio['followed'], profile_object['gender'], amount_query, buttons)
            elif chatbot_change > -30:
                answer = 'No. '
                increase_or_decrease = 'decrease by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(False, portfolio['followed'], profile_object['gender'], amount_query, buttons)
            else:
                answer = 'Absolutely not! '
                increase_or_decrease = 'decrease by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(False, portfolio['followed'], profile_object['gender'], amount_query, buttons)

            message = answer + 'I believe ' + profile_name.title() + '\'s portfolio will ' + increase_or_decrease + ' next month.'

        dispatcher.utter_button_message(message, buttons)

        return[]

    def appendButtons(self, positive, followed, gender, amount_query, buttons):
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
            buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
            buttons.append({"title": "Who should I stop following?", "payload": "Who should I stop following?"})


class ShouldIUnfollowAdvice(Action):
    def name(self):
        return 'action_should_i_unfollow_advice'

    def run(self, dispatcher, tracker, domain):
        username = tracker.current_state()["sender_id"]

        message = ''

        profile_name = tracker.get_slot('name')
        amount_query = tracker.get_slot('amount_query')

        buttons = []

        if profile_name is None:
            profile_name = tracker.latest_message['entities'][0]['value']

        if profile_name is None:
            message = "Sorry, I can't find that portfolio. Have you spelt the name correctly?"
        else:
            profile_request = requests.get(ROOT_URL + '/getprofiles/')
            profiles = profile_request.json()

            portfolio_request = requests.post(ROOT_URL + '/getportfolios/', data = {'username':username})
            portfolios = portfolio_request.json()

            profile_object = None
            for profile in profiles:
                if re.search(profile_name, profile['name'], re.IGNORECASE):
                    profile_object = profile
                    profile_name = profile['name']

            portfolio = None
            for p in portfolios:
                if p['profile_id'] == profile_object['id']:
                    portfolio = p

            chatbot_change = round(float(portfolio['chatbotNextChange']))

            answer = ''
            increase_or_decrease = ''

            if chatbot_change >= 30:
                answer = 'Absolutely not! '
                increase_or_decrease = 'increase by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(False, profile_object['gender'], amount_query, buttons)
            elif chatbot_change > 0:
                answer = 'No.'
                increase_or_decrease = 'increase by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(False, profile_object['gender'], amount_query, buttons)
            elif chatbot_change == 0:
                increase_or_decrease = 'not change'
                self.appendButtons(False, profile_object['gender'], amount_query, buttons)
            elif chatbot_change > -10:
                answer = 'Yes. '
                increase_or_decrease = 'decrease by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(True, profile_object['gender'], amount_query, buttons)
            elif chatbot_change > -30:
                answer = 'Yes. '
                increase_or_decrease = 'decrease by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(True, profile_object['gender'], amount_query, buttons)
            else:
                answer = 'Absolutely! '
                increase_or_decrease = 'decrease by ' + str(abs(chatbot_change)) + '%'
                self.appendButtons(True, profile_object['gender'], amount_query, buttons)

            message = answer + ' I believe ' + profile_name.title() + '\'s portfolio will ' + increase_or_decrease + ' next month.'

        dispatcher.utter_button_message(message, buttons)

        return[]

    def appendButtons(self, positive, gender, amount_query, buttons):
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
            buttons.append({"title": "Who should I follow?", "payload": "Who should i follow?"})
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

        requests.post(ROOT_URL + '/increasefallbackcount/', data = {'username':username})

        message = "Sorry, I didn't quite catch that."

        dispatcher.utter_message(message)

        return [UserUtteranceReverted()]
