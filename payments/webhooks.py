import stripe
from datetime import datetime


from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.utils import json

from miniblog import settings
from payments.models import MemberAccount


@csrf_exempt
@require_POST
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(e)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    event_data = event.data
    event_object = event.data.object
    try:
        member_account = MemberAccount.objects.filter(customer_id=event_object.customer)
    except MemberAccount.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    # Handle the event
    if event.type == 'customer.subscription.created':
        member_account.update(
            sub_id=event_object.id,
            account_type="Premium",
            subscription_end_date=datetime.fromtimestamp(event_object.current_period_end).strftime('%Y-%m-%d'),
            active_subscription=True if event_object.status == 'active' else False
        )

    elif event.type == 'customer.subscription.updated':
        member_account.update(
            sub_id=event_object.id,
            account_type="Premium",
            subscription_end_date=datetime.fromtimestamp(event_object.current_period_end).strftime('%Y-%m-%d'),
            active_subscription=True if event_object.status == 'active' else False
        )

    elif event.type == 'customer.subscription.pending_update_applied':
        member_account.update(
            sub_id=event_object.id,
            account_type="Premium",
            subscription_end_date=datetime.fromtimestamp(event_object.current_period_end).strftime('%Y-%m-%d'),
            active_subscription=True if event_object.status == 'active' else False
        )

    elif event.type == 'customer.subscription.pending_update_expired':
        member_account.update(
            sub_id=event_object.id,
            active_subscription=False
        )

    elif event.type == 'customer.subscription.deleted':
        member_account.update(
            sub_id=event_object.id,
            account_type="Standard",
            subscription_end_date=None,
            active_subscription=False
        )

    print(event.type)
    return HttpResponse(status=200)
