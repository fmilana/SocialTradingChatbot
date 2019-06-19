from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

# from.django.core import serializers
from django.contrib.auth.models import User
from .models import Profile, Portfolio, Newspost, Balance, InvestedBalance

from django.core import serializers


def welcome_page(request):
    return render(request, 'welcome.html')


def chatbot_page(request):
    profiles = Profile.objects.all()
    image_names = []

    for profile in profiles:
        image_names.append(profile.name.replace(' ', '-') + ".jpg")

    context = {
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
