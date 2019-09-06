# coding: utf-8
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

from chatbot.models import Message
from django.contrib.auth.models import User

@csrf_exempt
@require_POST
def webhook_view(request):
    client_data = json.loads(request.body.decode('utf-8'))
    # localhost:5005/webhooks/rest/webhook
    url = "http://localhost:5500/webhooks/rest/webhook"
    # TODO: get json data from the request
    # print('client_data:', client_data)
    json_data = json.dumps(client_data)
    # json_data = client_data

    periodic_advice = client_data["periodic_advice"]

    # save user message on db
    if not periodic_advice:
        user = User.objects.get(username=client_data["sender"])
        month = client_data["month"]
        from_notification = client_data["from_notification"]
        from_button = client_data["from_button"]
        text = client_data["message"]

        message = Message(user=user, month=month, from_participant=True, from_button=from_button, text=text)
        message.save()

    proxy_response = requests.post(url, data=json_data)
    print('status code:', proxy_response.status_code)
    print('content:', proxy_response.content)

    return HttpResponse(proxy_response.content, content_type='application/json')
