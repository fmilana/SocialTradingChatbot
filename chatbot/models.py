from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Profile(models.Model):
    name = models.TextField(null=False)
    gender = models.TextField()


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', null=True, on_delete=models.CASCADE)
    followed = models.BooleanField(default=False)
    risk = models.IntegerField(null=False)
    invested = models.DecimalField(max_digits=6, decimal_places=2)
    lastChange = models.DecimalField(max_digits=5, decimal_places=2)


class Newspost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', null=True, on_delete=models.PROTECT)
    text = models.TextField()

    def asJson(self):
        return dict(
            profile=self.profile,
            text=self.text,
            user=self.user)


class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=1000.00)


class InvestedBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def amount(self):
        return Portfolio.objects.filter(followed=True).aggregate(Sum('invested')).get('invested__sum')


class Month(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
