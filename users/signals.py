import stripe
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import UserProfile
from payments.models import MemberAccount


@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)  # , avatar='/avatar.png')

        stripe_customer = stripe.Customer.create(
            email=instance.email,
            name=instance.get_full_name()
        )

        member_account = MemberAccount.objects.create(user=instance, customer_id=stripe_customer.id)
