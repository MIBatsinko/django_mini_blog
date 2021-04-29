import stripe
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models, IntegrityError, transaction
from django.dispatch import receiver

from blog.models import UserProfile
from miniblog import settings
from payments.models import MemberAccount


@receiver(post_save, sender=User)
def create_userprofile(sender, instance, **kwargs):
    try:  # <-- need?
        # Fixed: django.db.transaction.TransactionManagementError:
        # An error occurred in the current transaction.
        # You can't execute queries until the end of the 'atomic' block.
        with transaction.atomic():
            userprofile = UserProfile.objects.create(user=instance, avatar='/avatar.png')
            userprofile.save()
    except IntegrityError:
        pass


@receiver(post_save, sender=User)
def create_member_account(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            if not MemberAccount.objects.filter(user_id=instance).exists():
                stripe.api_key = settings.STRIPE_SECRET_KEY
                stripe_customer = stripe.Customer.create(
                    description="My First Test Customer (created for API docs)",
                    email=instance.email,
                    name=instance.get_full_name()
                )
                stripe_customer.save()
                member_account = MemberAccount.objects.create(user_id=instance, customer_id=stripe_customer.id)
                member_account.save()
    except IntegrityError:
        pass
