from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template


def welcome_page(request):
    return render(request, "welcome.html")


def chatbot_page(request):
    return render(request, "chatbot.html")


def imagetagging_page(request):
    return render(request, "imagetagging.html")

# def example_page(request):
#     # context = {"title":"Example"}
#     template_name = "home.html"
#     template_obj = get_template(template_name)
#
#     return HttpResponse(template_obj.render(context))
