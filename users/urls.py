from django.urls import path

from users.views import UserApiView, SingleUserApiView

urlpatterns = [
    path('', UserApiView.as_view(), name='view_users'),
    path('<int:pk>/', SingleUserApiView.as_view(), name='view_user'),
]
