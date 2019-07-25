from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Profile(models.Model):
    name = models.TextField(null=False)
    gender = models.TextField()

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', null=True, on_delete=models.CASCADE)
    followed = models.BooleanField(default=False)
    risk = models.IntegerField(null=False)
    invested = models.DecimalField(max_digits=6, decimal_places=2)
    lastChange = models.DecimalField(max_digits=5, decimal_places=2)
    chatbotNextChange = models.DecimalField(max_digits=5, decimal_places=2)
    newspostNextChange = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = 'Portfolio'
        verbose_name_plural = 'Portfolios'

    def __str__(self):
        return self.user.username + "-" + self.profile.name


class Newspost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', null=True, on_delete=models.PROTECT)

    def asJson(self):
        return dict(
            profile=self.profile,
            user=self.user)

    class Meta:
        verbose_name = 'Newspost'
        verbose_name_plural = 'Newsposts'

    def __str__(self):
        return self.user.username + "-" + self.profile.name


class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=1000.00)

    class Meta:
        verbose_name = 'Balance'
        verbose_name_plural = 'Balances'

    def __str__(self):
        return self.user.username


class InvestedBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    @property
    def amount(self):
        if not Portfolio.objects.filter(user=self.user, followed=True):
            return 0.0
        else:
            return round(Portfolio.objects.filter(user=self.user, followed=True).aggregate(Sum('invested')).get('invested__sum'), 2)

    class Meta:
        verbose_name = 'Invested Balance'
        verbose_name_plural = 'Invested Balances'

    def __str__(self):
        return self.user.username


class Month(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Month'
        verbose_name_plural = 'Months'

    def __str__(self):
        return self.user.username
