"""chatbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import include


from .views import (
    welcome_page,
    chatbot_page,
    update_month,
    update_portfolios,
    update_balances,
    # update_followed,
    # imagetagging_page,
    )

urlpatterns = [
    url(r'^$', welcome_page, name='welcome'),
    url(r'^chatbot/$', chatbot_page, name='chatbot'),
    url(r'^imagetagging/', include('imagetagging.urls'), name='imagetagging'),
    url(r'^updatemonth/', update_month, name='updatemonth'),
    url(r'^updateportfolios/', update_portfolios, name='updateportfolios'),
    url(r'^updatebalances/', update_balances, name='updatebalances'),
    # url(r'^updatefollowed/', update_followed, name='updatefollowed'),
    url(r'^admin/', admin.site.urls),
]
