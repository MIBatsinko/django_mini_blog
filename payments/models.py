from django.contrib.auth.models import User
from django.db import models


class MemberAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_id = models.CharField(null=True, max_length=255)
    sub_id = models.CharField(null=True, max_length=255)
    account_type = models.CharField(default="Standard", max_length=255)  # or Premium
    subscription_end_date = models.DateTimeField(null=True, blank=True)
    active_subscription = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
