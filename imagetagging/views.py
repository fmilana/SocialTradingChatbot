from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.db.utils import IntegrityError
from .djutils import to_dict, log_request
from .forms import TagForm
from .models import Tag, ImageTask
# from study.models import Participant
import json


@login_required
@require_GET
@log_request
def image_task(request, image_task_id=None):
    if image_task_id is None:
        # TODO get the first image
        image_task_id = ImageTask.objects.all().order_by('image')[0].id
    # return the image
    image_task = get_object_or_404(ImageTask, id=image_task_id)
    data = to_dict(image_task)
    data['image_url'] = image_task.image.url
    data['tags'] = [t.label for t in Tag.objects.filter(image_task=image_task, user=request.user, correct=True)]
    print(json.dumps(data))
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
@require_POST
@log_request
def tags(request):

    print('tag called')

    form = TagForm(request.POST)
    if not form.is_valid():
        print(form.errors.as_json())
        return HttpResponseBadRequest(form.errors.as_json(), content_type='application/json')

    tag = form.save(commit=False)
    tag.user = request.user

    # check whether the tag is in the groundtruth
    master_tag_objects = Tag.objects.filter(user__is_superuser=True, image_task=tag.image_task)
    master_tags = set(master_tag_objects.values_list('label', flat=True))

    if tag.label not in master_tags:
        # save the tag
        try:
            tag.save()
        except IntegrityError:
            # ignore duplicates
            pass
        return HttpResponse(json.dumps({'correct': False}), content_type='application/json')

    # the tag is correct!
    tag.correct = True
    # try to save it -- if we don't throw an exception it means it's all good
    try:
        tag.save()
    except IntegrityError:
        response = {'correct': False, 'reason': 'duplicate'}
        return HttpResponse(json.dumps(response), content_type='application/json')

    # if we get here, it means save worked fine
    response = {'correct': True}

    # check whether now the user has 3 correct tags for this image
    correct_count = Tag.objects.filter(image_task=tag.image_task, user=request.user, correct=True).count()
    if correct_count == 3:
        response['complete'] = True

        # increment the participant's earned
        # participant = Participant.objects.get(user=request.user)
        # earned_increase = participant.condition.labour_task_reward
        # participant.earned += earned_increase
        # participant.tasks_completed += 1
        # print(participant.tasks_completed)
        # participant.save()
    elif correct_count > 3:
        response['complete'] = True
    else:
        response['complete'] = False

    return HttpResponse(json.dumps(response), content_type='application/json')
