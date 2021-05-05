from django.urls import path

from payments.views import HomePageView, CancelSubscription, CancelledView, SuccessView, stripe_config, create_checkout_session
from payments.webhooks import stripe_webhook

urlpatterns = [
    path('', HomePageView.as_view(), name='premium'),
    path('config/', stripe_config),
    path('create-checkout-session/', create_checkout_session, name='create_session'),
    path('success/', SuccessView.as_view()),
    path('cancelled/', CancelledView.as_view()),
    path('webhook/', stripe_webhook),
    path('cancel/', CancelSubscription.as_view(), name='cancel_sub')
]
