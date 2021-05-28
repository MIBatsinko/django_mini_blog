from django.urls import path
import my_account.views as views
from allauth.account import views as allauth_views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='my_account_login'),
    path('register/', views.SignupView.as_view(), name='my_account_signup'),
    path('logout/', views.LogoutView.as_view(), name='my_account_logout'),
    path('password_reset/', allauth_views.PasswordResetView.as_view(), name='my_account_reset_password'),
    path('password_reset_done/', allauth_views.PasswordResetDoneView.as_view(), name='my_account_password_reset_done'),
    path('password_reset_from_key/', allauth_views.PasswordResetFromKeyView.as_view(), name='my_account_password_reset_from_key'),
    path('password_reset_from_key_done/', allauth_views.PasswordResetFromKeyDoneView.as_view(), name='my_account_password_reset_from_key_done'),
    path('password_set/', allauth_views.PasswordSetView.as_view(), name='my_account_password_set'),
]
