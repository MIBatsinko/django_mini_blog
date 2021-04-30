from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveUpdateAPIView

from miniblog import settings
from .serializers import UserSerializer, UserResponseSerializer, SingleUserSerializer


class UserApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']

    @swagger_auto_schema(responses={status.HTTP_200_OK: UserResponseSerializer()})
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@method_decorator(login_required(login_url='my_account_login'), name='dispatch')
class SingleUserApiView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = SingleUserSerializer
