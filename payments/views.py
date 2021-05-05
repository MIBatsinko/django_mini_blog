import stripe
from datetime import datetime
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateView
from rest_framework import status
from rest_framework.utils import json

from payments.models import MemberAccount


class HomePageView(TemplateView):
    template_name = 'payments/premium.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        try:
            stripe_customer = MemberAccount.objects.get(user=self.request.user)
            context['stripe_customer'] = stripe_customer
            return context

        except MemberAccount.DoesNotExist:
            return context
        except stripe.error.InvalidRequestError:
            return context
        except TypeError:
            return context


class SuccessView(TemplateView):
    template_name = 'payments/success.html'


class CancelledView(TemplateView):
    template_name = 'payments/cancelled.html'


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'https://987b48351186.ngrok.io/payments/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='subscription',
                customer=request.user.memberaccount.customer_id,
                line_items=[
                    {
                        'quantity': 1,
                        'price': settings.STRIPE_PRICE_ID,
                    }
                ],

            )
            return JsonResponse({'session_id': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
@require_POST
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
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


class CancelSubscription(HomePageView):
    template_name = 'payments/cancel_sub.html'

    def get_context_data(self, **kwargs):
        context = super(CancelSubscription, self).get_context_data(**kwargs)
        MemberAccount.objects.filter(user=self.request.user).update(active_subscription=False)
        return context
