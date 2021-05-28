import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from rest_framework import status

from payments.models import MemberAccount
from payments.services.stripe_service import Stripe


class HomePageView(TemplateView):
    template_name = 'payments/premium.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        try:
            stripe_customer = MemberAccount.objects.get(user=self.request.user)
            context['stripe_customer'] = stripe_customer
            return context

        except Exception as e:
            print(e)
            return context


class SuccessView(TemplateView):
    template_name = 'payments/success.html'


class CancelledView(TemplateView):
    template_name = 'payments/cancelled.html'


# @csrf_exempt
# def stripe_config(request):
#     if request.method == 'GET':
#         stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
#         return JsonResponse(stripe_config, safe=False)
#

@csrf_exempt
@login_required
def create_checkout_session(request):
    if request.method == 'GET':
        stripe_service = Stripe(user=request.user)
        session_id = stripe_service.create_session()
        if session_id:
            return JsonResponse({'session_id': session_id})
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


class CancelSubscription(HomePageView):
    template_name = 'payments/cancel_sub.html'

    def get_context_data(self, **kwargs):
        context = super(CancelSubscription, self).get_context_data(**kwargs)
        MemberAccount.objects.filter(user=self.request.user).update(active_subscription=False)
        return context
