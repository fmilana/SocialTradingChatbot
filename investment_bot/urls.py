# coding: utf-8
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    # url(r'^updatefollowed/', update_followed, name='updatefollowed'),
    url(r'^admin/', admin.site.urls),

    path('chatbotproxy/', include('chatbotproxy.urls')),
    path('', include('chatbot.urls')),

]
