import stripe
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models, IntegrityError, transaction
from django.dispatch import receiver

from blog.models import UserProfile
from miniblog import settings
from payments.models import MemberAccount


@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance, avatar='/avatar.png')
        userprofile.save()

        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe_customer = stripe.Customer.create(
            email=instance.email,
            name=instance.get_full_name()
        )
        stripe_customer.save()

        member_account = MemberAccount.objects.create(user=instance, customer_id=stripe_customer.id)
        member_account.save()
