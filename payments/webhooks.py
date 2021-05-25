import stripe
from datetime import datetime
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import status

from miniblog import settings
from payments.models import MemberAccount


@csrf_exempt
@require_POST
def stripe_webhook(request):
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
        print(e)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(e)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    event_data = event.data
    event_object = event.data.object
    try:
        member_account = MemberAccount.objects.filter(customer_id=event_object.customer)
        print(member_account)
        print(event_object.customer)
    except MemberAccount.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except AttributeError as e:
        print("Error :", e)

    # Handle the event
    if event.type in ['customer.subscription.created',
                      'customer.subscription.updated',
                      'customer.subscription.pending_update_applied']:
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
            active_subscription=False
        )
    elif event.type in ['charge.succeeded', 'charge.updated']:
        fingerprint = event_object.get('payment_method_details').get('card').get('fingerprint')
        last4 = event_object.get('payment_method_details').get('card').get('last4')
        card_id = event_object.get('payment_method')

        member_account.update(card_id=last4)
        print(event_object.get('payment_method'))
        print(card_id)
        print(last4)
        print(fingerprint)

    print(event.type)
    return HttpResponse(status=status.HTTP_200_OK)
