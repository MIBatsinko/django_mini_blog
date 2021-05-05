import stripe
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

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


class CancelSubscription(HomePageView):
    template_name = 'payments/cancel_sub.html'

    def get_context_data(self, **kwargs):
        context = super(CancelSubscription, self).get_context_data(**kwargs)
        MemberAccount.objects.filter(user=self.request.user).update(active_subscription=False)
        return context
