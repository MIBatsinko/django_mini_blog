from allauth.account.views import PasswordResetView, PasswordResetDoneView, PasswordResetFromKeyView, \
    PasswordResetFromKeyDoneView, PasswordSetView
from django.urls import path

from my_account.views import LoginView, SignupView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='my_account_login'),
    path('register/', SignupView.as_view(), name='my_account_signup'),
    path('logout/', LogoutView.as_view(), name='my_account_logout'),
    path('password_reset/', PasswordResetView.as_view(), name='my_account_reset_password'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='my_account_password_reset_done'),
    path('password_reset_from_key/', PasswordResetFromKeyView.as_view(), name='my_account_password_reset_from_key'),
    path('password_reset_from_key_done/', PasswordResetFromKeyDoneView.as_view(), name='my_account_password_reset_from_key_done'),
    path('password_set/', PasswordSetView.as_view(), name='my_account_password_set'),
]
