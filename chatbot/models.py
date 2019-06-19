from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Profile(models.Model):
    name = models.TextField(null=False)
    gender = models.TextField()


class Portfolio(models.Model):
    profile = models.ForeignKey('Profile', null=True, on_delete=models.CASCADE)
    followed = models.BooleanField(default=False)
    risk = models.IntegerField(null=False)
    invested = models.DecimalField(max_digits=6, decimal_places=2)
    lastChange = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Newspost(models.Model):
    profile = models.ForeignKey('Profile', null=True, on_delete=models.PROTECT)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def asJson(self):
        return dict(
            profile=self.profile,
            text=self.text,
            user=self.user)


class Balance(models.Model):
    # amount = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def amount(self):
        return 1000 - InvestedBalance.objects.first().amount


class InvestedBalance(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # @property
    # def amount(self):
    #     return Portfolio.objects.filter(followed=True).aggregate(Sum(invested))


class Month(models.Model):
    number = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
