from django.urls import path
from . import views

urlpatterns = [
    path(r'tags/', views.tags, name='tags'),
    path(r'image-task/<int:image_task_id>/', views.image_task, name='image_task'),
    # TODO check that this is ok
    path(r'image-task/', views.image_task, name='image_task'),
]
