from django.urls import path

from users.views import UserApiView, SingleUserApiView, SingleUserUpdateApiView

urlpatterns = [
    path('', UserApiView.as_view(), name='view_users'),
    path('edit/', SingleUserUpdateApiView.as_view(), name='edit_user'),
    path('<int:pk>/', SingleUserApiView.as_view(), name='view_user'),
]
