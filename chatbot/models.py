from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Condition(models.Model):
    active = models.BooleanField(default=True, null=False)

    def __str__(self):
        return "Condition"


class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    condition_active = models.BooleanField(default=True, null=False)

    class Meta:
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    name = models.CharField(max_length=128, null=False)
    gender = models.CharField(max_length=128, null=False)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.name


class Month(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField(default=1, null=False)

    class Meta:
        verbose_name = 'Month'
        verbose_name_plural = 'Months'

    def __str__(self):
        return self.user.username


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


class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    available = models.DecimalField(max_digits=6, decimal_places=2, default=1000.00)

    @property
    def invested(self):
        if not Portfolio.objects.filter(user=self.user, followed=True):
            return 0.0
        else:
            return round(Portfolio.objects.filter(user=self.user, followed=True).aggregate(Sum('invested')).get('invested__sum'), 2)

    class Meta:
        verbose_name = 'Balance'
        verbose_name_plural = 'Balances'

    def __str__(self):
        return self.user.username


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.IntegerField(null=False)
    from_participant = models.BooleanField(null=False)
    from_notification = models.BooleanField(null=False, default=False)
    from_button = models.BooleanField(null=False, default=False)
    text = models.TextField(null=False)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        if self.from_participant:
            return self.user.username + ': ' + self.text
        else:
            return self.user.username + ', Bot: ' + self.text


class UserAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.IntegerField(default=1, null=False)
    available = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    invested = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    portfolio = models.CharField(max_length=128, null=False)
    chatbot_change = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    newspost_change = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    action = models.CharField(max_length=128, null=False)
    amount = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    class Meta:
        verbose_name = 'User Action'
        verbose_name_plural = 'User Actions'

    def __str__(self):
        return self.user.username + ': ' + self.action + " (" + str(self.amount) + ") " + self.portfolio


class DismissNotificationCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(default=0, null=False)

    class Meta:
        verbose_name = 'Dismiss Notification Count'
        verbose_name_plural = 'Dismiss Notification Counts'

    def __str__(self):
        return self.user.username
