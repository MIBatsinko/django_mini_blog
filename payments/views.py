import stripe
from datetime import datetime
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from rest_framework.utils import json

from payments.models import MemberAccount


class HomePageView(TemplateView):
    template_name = 'payments/premium.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        try:
            stripe_customer = MemberAccount.objects.get(user_id=self.request.user)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            subscription = stripe.Subscription.retrieve(stripe_customer.sub_id)
            product = stripe.Product.retrieve(subscription.plan.product)
            context['subscription'] = subscription
            context['product'] = product
            context['sub_end'] = datetime.fromtimestamp(subscription.current_period_end).strftime('%Y-%m-%d %H:%M:%S')
            return context

        except MemberAccount.DoesNotExist:
            return context
        except stripe.error.InvalidRequestError:
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
        domain_url = 'https://c0cc685d4ac6.ngrok.io/payments/'
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
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
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
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'subscription_intent.created':
        payment_intent = event.data.object
    elif event.type == 'charge.succeeded':
        charge = event.data.object
    elif event.type == 'customer.subscription.created':
        sub_created = event.data.object
        print(sub_created.current_period_end)
        member_account = MemberAccount.objects.filter(customer_id=sub_created.customer).update(
            sub_id=sub_created.id,
            account_type="Premium",
            subscription_end_date=datetime.fromtimestamp(sub_created.current_period_end).strftime('%Y-%m-%d %H:%M:%S'),
            active_subscription=True
        )
        member_account.save()
    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)
