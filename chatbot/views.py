from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

# from.django.core import serializers
from django.contrib.auth.models import User
from .models import Profile, Portfolio, Newspost, Balance, InvestedBalance, Month

from django.core import serializers

import json

from random import gauss
import decimal


def welcome_page(request):
    return render(request, 'welcome.html')


def chatbot_page(request):
    profiles = Profile.objects.all()
    image_names = []

    for profile in profiles:
        image_names.append(profile.name.replace(' ', '-') + ".jpg")

    context = {
        'month_number': Month.objects.first().number,
        'available_balance_amount': Balance.objects.first().amount,
        'invested_balance_amount': InvestedBalance.objects.first().amount,
        'image_names': image_names,
        'profiles': serializers.serialize('json', Profile.objects.all()),
        'followed_portfolios': Portfolio.objects.filter(followed=True),
        'not_followed_portfolios': Portfolio.objects.filter(followed=False),
        'newsposts': serializers.serialize('json', Newspost.objects.all()),
        }

    return render(request, 'chatbot.html', context)


def imagetagging_page(request):
    context = {
        'available_balance_amount': Balance.objects.first().amount,
        'invested_balance_amount': InvestedBalance.objects.first().amount,
        }

    return render(request, 'imagetagging.html', context)


def update_month(request):
    month = Month.objects.first()

    if month.number < 5:
        month.number += 1
        month.save()

        response = {'increased': True, 'month': str(month.number)}
    else:
        response = {'increased': False}

    return HttpResponse(json.dumps(response), content_type="application/json")


def update_portfolios(request):

    response = {}

    for portfolio in Portfolio.objects.all():
        change_value = gauss(0.0, portfolio.risk*5)

        portfolio.lastChange = round(change_value, 2)

        change_value /= 100
        change_value += 1

        if portfolio.followed:
            new_invested_amount = round(portfolio.invested * decimal.Decimal(change_value), 2)

            portfolio.invested = new_invested_amount

        portfolio.save()

        response[portfolio.profile.name] = change_value

    response['invested_balance_amount'] = str(InvestedBalance.objects.first().amount)

    return HttpResponse(json.dumps(response), content_type="application/json")



# def update_followed(request):
#     print('update_followed called')
#
#     followed_portfolios = Portfolio.objects.filter(followed=True)
#     not_followed_portfolios = Portfolio.objects.filter(followed=False)
#
#     response = {'followed': followed_portfolios, 'not_followed': not_followed_portfolios}
#
#     return HttpResponse(json.dumps(response), content_type="application/json")
