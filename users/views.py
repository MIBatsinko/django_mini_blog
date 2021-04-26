from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .serializers import UserSerializer, UserResponseSerializer, SingleUserSerializer


class UserApiView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']

    @swagger_auto_schema(responses={status.HTTP_200_OK: UserResponseSerializer()})
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @swagger_auto_schema(responses={status.HTTP_200_OK: UserResponseSerializer()})
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SingleUserApiView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = SingleUserSerializer
