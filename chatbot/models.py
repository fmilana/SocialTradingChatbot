from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    image = models.ImageField()
    name = models.TextField()
    gender = models.TextField()

class Portfolio(models.Model):
    profile = models.ForeignKey('Profile', null=True, on_delete=models.CASCADE)
    followed = models.BooleanField(default=False)
    invested = models.DecimalField(max_digits=6, decimal_places=2)
    lastChange = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class NewsPost(models.Model):
    profile = models.ForeignKey('Profile', null=True, on_delete=models.PROTECT)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Balance(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class InvestedBalance(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Month(models.Model):
    number = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
