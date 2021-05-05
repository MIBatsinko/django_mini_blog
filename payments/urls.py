from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='premium'),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session, name='create_session'),
    path('success/', views.SuccessView.as_view()),
    path('cancelled/', views.CancelledView.as_view()),
    path('webhook/', views.stripe_webhook),
    path('cancel/', views.CancelSubscription.as_view(), name='cancel_sub')
]
