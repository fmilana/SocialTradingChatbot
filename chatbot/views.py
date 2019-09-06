# coding: utf-8
import json
import random
from random import gauss, randrange
import decimal
import os

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime
from django.core import serializers
from django.db import IntegrityError

from .djutils import to_dict

from .models import Profile, Portfolio, Balance, Month, Message, Participant, \
    Condition, Result, QuestionnaireResponse, FallbackCount


def welcome_page(request):
    return render(request, 'welcome.html')


def information_page(request):
    return render(request, 'information.html')


def consent_page(request):
    return render(request, 'consent.html')


def instructions_page(request):
    return render(request, 'instructions.html')


@login_required
def results_page(request):
    user = request.user
    result1 = Result.objects.get(user=user, month=1)
    result2 = Result.objects.get(user=user, month=2)
    result3 = Result.objects.get(user=user, month=3)
    result4 = Result.objects.get(user=user, month=4)
    result5 = Result.objects.get(user=user, month=5)

    context = {
        'month_1_total': result1.total,
        'month_1_profit': result1.profit,
        'month_1_images_tagged': float(result1.images_tagged*10),
        'month_2_total': result2.total,
        'month_2_profit': result2.profit,
        'month_2_images_tagged': float(result2.images_tagged*10),
        'month_3_total': result3.total,
        'month_3_profit': result3.profit,
        'month_3_images_tagged': float(result3.images_tagged*10),
        'month_4_total': result4.total,
        'month_4_profit': result4.profit,
        'month_4_images_tagged': float(result4.images_tagged*10),
        'month_5_total': result5.total,
        'month_5_profit': result5.profit,
        'month_5_images_tagged': float(result5.images_tagged*10),
        'final_score': result5.total - 1000
        }

    return render(request, 'results.html', context)


@csrf_exempt
@require_POST
def participants_view(request):
    username = request.POST['username']
    is_test_user = False
    if username == "TEST":
        username = "TEST_USER__{}".format(datetime.strftime(datetime.now(), '%Y_%m_%d__%H_%M_%S'))
        is_test_user = True
    try:
        user = User.objects.create_user(username=username)
        month = Month(user=user, number=1)
        month.save()

        for profile in Profile.objects.all():
            risk = randrange(9)+1

            chatbot_change = gauss(0.0, risk*5)

            if chatbot_change >= 100:
                chatbot_change = 99
            elif chatbot_change <= -100:
                chatbot_change = -99

            newspost_change = gauss(0.0, risk*5)

            if newspost_change >= 100:
                newspost_change = 99
            elif newspost_change <= -100:
                newspost_change = -99

            portfolio = Portfolio(user=user, profile=profile, followed=False, risk=risk, invested=0.00, lastChange=0.00, chatbotNextChange=chatbot_change, newspostNextChange=newspost_change)

            portfolio.save()

        balance = Balance(user=user, available=1000.00)
        balance.save()

        result = Result(user=user, month=1, profit=0.00, images_tagged=0, total=1000.00)
        result.save()

        # dismiss_notification_count = DismissNotificationCount(user=user, count=0)
        # dismiss_notification_count.save()

        fallback_count = FallbackCount(user=user, count=0)
        fallback_count.save()

    except IntegrityError:
        error = {
            "username": [{"message": "This field is duplicate.", "code": "duplicate"}]
            }
        data = json.dumps(error)
        return HttpResponseBadRequest(data, content_type='application/json')

    condition = Condition.objects.first()
    condition_active = condition.active

    participant = Participant(user=user, condition_active=condition_active)
    participant.save()

    if condition_active:
        condition.active = False
    else:
        condition.active = True

    condition.save()

    # # TODO: create participant
    # participant = Participant()
    # participant.user = user
    # participant.created_for_testing = is_test_user
    # # TODO: assign condition or task list
    # all_task_lists = TaskList.objects.filter(active=True
    #     ).annotate(n_participants=Count('participant')
    #     ).order_by('n_participants')
    # participant.task_list = all_task_lists[0]
    # participant.save()
    login(request, user)

    #data = json.dumps(to_dict(participant, transverse=True))
    data = json.dumps(to_dict(user, transverse=False))
    return HttpResponse(data, content_type='application/json')


@login_required
def get_condition_active(request):
    user = request.user

    condition_active = Participant.objects.get(user=user).condition_active

    response = {'condition_active': condition_active}

    return HttpResponse(json.dumps(response), content_type="application/json")


# @csrf_exempt
# @login_required
# def update_dismiss_notification_count(request):
#     user = request.user
#
#     dismiss_notification_count = DismissNotificationCount.objects.get(user=user)
#     dismiss_notification_count.count += 1
#     dismiss_notification_count.save()
#
#     return HttpResponse("")


@login_required
def chatbot_page(request):
    user = request.user
    profiles = Profile.objects.all()
    image_names = []

    for profile in profiles:
        image_names.append(profile.name.replace(' ', '-') + ".jpg")

    context = {
        'available_balance_amount': format(Balance.objects.get(user=user).available, '.2f'),
        'invested_balance_amount': format(Balance.objects.get(user=user).invested, '.2f'),
        'image_names': image_names,
        'profiles': serializers.serialize('json', Profile.objects.all()),
        'followed_portfolios': Portfolio.objects.filter(user=user, followed=True),
        'not_followed_portfolios': Portfolio.objects.filter(user=user, followed=False),
        }

    return render(request, 'chatbot.html', context)


@login_required
def imagetagging_page(request):
    user = request.user
    balance = Balance.objects.get(user=user)
    context = {
        'available_balance_amount': balance.available,
        'invested_balance_amount': balance.invested,
        }

    return render(request, 'imagetagging.html', context)


@login_required
def update_portfolios(request):
    user = request.user
    response = {}

    for portfolio in Portfolio.objects.filter(user=user):
        next_change = random.choice([portfolio.chatbotNextChange, portfolio.newspostNextChange])

        portfolio.lastChange = round(next_change, 2)

        next_change /= 100
        next_change += 1

        if portfolio.followed:
            new_invested_amount = round(portfolio.invested * decimal.Decimal(next_change), 2)
            portfolio.invested = new_invested_amount

        portfolio.save()

    balance = Balance.objects.get(user=user)

    response['available_balance_amount'] = str(balance.available)
    response['invested_balance_amount'] = str(balance.invested)

    generate_next_portfolio_changes(request)

    return HttpResponse(json.dumps(response), content_type="application/json")


@csrf_exempt
@login_required
def update_results(request):
    user = request.user
    month = int(request.POST['month'])
    profit = float(request.POST['profit'])
    total = float(request.POST['total'])

    print('GETTING RESULT OBJECT WITH MONTH = ' + str(month))
    print('profit = ' + str(profit))
    print('total = ' + str(total))

    result = Result.objects.get(user=user, month=month)
    result.profit = profit
    result.total = total
    result.save()

    return HttpResponse("")


@login_required
def update_balances(request):
    user = request.user
    response = {}

    balance = Balance.objects.get(user=user)

    response['available_balance_amount'] = str(balance.available)
    response['invested_balance_amount'] = str(balance.invested)

    if response['available_balance_amount'] == '0.0':
        response['available_balance_amount'] = '0.00'

    if response['invested_balance_amount'] == '0.0':
        response['invested_balance_amount'] = '0.00'

    print(response)

    return HttpResponse(json.dumps(response), content_type="application/json")


@csrf_exempt
@login_required
def update_month(request):
    user = request.user
    month = Month.objects.get(user=user)

    response = {}

    if month.number < 5:
        month.number += 1
        month.save()

        result = Result(user=user, month=month.number, profit=0.00, images_tagged=0, total=0.00)
        result.save()

        response['has_increased'] = True
    else:
        response['has_increased'] = False

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def get_next_changes(request):
    user = request.user
    response = {}

    for portfolio in Portfolio.objects.filter(user=user):
        response[portfolio.profile.name + '-chatbot-change'] = float(portfolio.chatbotNextChange)
        response[portfolio.profile.name + '-newspost-change'] = float(portfolio.newspostNextChange)

    return HttpResponse(json.dumps(response), content_type="application/json")


@csrf_exempt
@login_required
def store_bot_message(request):
    user = request.user
    month = request.POST['month']
    text = request.POST['text']

    message = Message(user=user, month=month, from_participant=False, from_button=False, text=text)
    message.save()

    return HttpResponse("")


@login_required
def generate_next_portfolio_changes(request):

    user = request.user
    for portfolio in Portfolio.objects.filter(user=user):

        chatbot_change = gauss(0.0, portfolio.risk*5)

        if chatbot_change >= 100:
            chatbot_change = 99
        elif chatbot_change <= -100:
            chatbot_change = -99

        newspost_change = gauss(0.0, portfolio.risk*5)

        if newspost_change >= 100:
            newspost_change = 99
        elif newspost_change <= -100:
            newspost_change = -99

        portfolio.chatbotNextChange = chatbot_change
        portfolio.newspostNextChange = newspost_change

        portfolio.save()


@csrf_exempt
@require_http_methods(['GET', 'POST'])
@login_required
def questionnaire_view(request):
    if request.method == 'GET':
        questionnaire = '''[
    {'label': '<hr><h5>Please answer the following questions <u>based on your overall experience</u> completing the study</h5><hr>'},
    {'question': '1. From 1 to 5, how much did you trust the <strong>Assistant</strong> by the end of the study?', choices: ['1', '2', '3', '4', '5']},
    {'question': '2. From 1 to 5, how much did you trust the <strong>Newsfeed</strong> by the end of the study?', choices: ['1', '2', '3', '4', '5']},
    {'question': '3. From 1 to 5, how often did the <strong>Assistant</strong> understand what you said?', choices: ['1', '2', '3', '4', '5']},
    {'question': '4. What would have made you trust the <strong>Assistant</strong> more?'},
    {'question': '5. Please leave your comments about your experience interacting with the <strong>Assistant</strong>.'},
    {'question': '<hr>Please leave your comments about the overall experience about this study, or your suggestions for improvement.'}
        ]
        '''
        context = {
            'questionnaire': questionnaire,
        }
        template_path = 'questionnaire.html'
        return render(request, template_path, context=context)
    elif request.method == 'POST':
        # TODO: store the result(s) and render/redirect to the next page
        post_data = json.loads(request.body.decode('utf-8'))
        questionnaire_response = QuestionnaireResponse(
            user = request.user,
            answer = post_data['groups'],
            completion_time = post_data['task_completion_time'],
            subtask_time = post_data['log']
        )
        questionnaire_response.save()

        # TODO: redirect to some end page
        # https://app.prolific.ac/submissions/complete?cc=J8OWBL27
        #study_settings = StudySettings.load()
        #study_id = study_settings.prolific_study_id
        # TODO: Fix this url
        result = {
            'completion_url': 'https://app.prolific.co/submissions/complete?cc=5E140EBC'
        }# https://app.prolific.ac/submissions/complete?cc=' + study_id
        result_data = json.dumps(result)
        return HttpResponse(result_data, content_type='application/json')

        #return redirect(completion_url)
        # return HttpResponse('the end')
