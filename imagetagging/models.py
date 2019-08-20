from django.db import models
from django.contrib.auth.models import User


class ImageTask(models.Model):
    image = models.ImageField()
    next_task = models.ForeignKey('ImageTask', null=True, on_delete=models.SET_NULL)

class GroundTruthTag(models.Model):
    image_task = models.ForeignKey(ImageTask, on_delete=models.CASCADE)
    label = models.CharField(max_length=128)

    class Meta:
        unique_together = ('image_task', 'label')

class Tag(models.Model):
    image_task = models.ForeignKey(ImageTask, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=128)
    correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ('image_task', 'user', 'label')
