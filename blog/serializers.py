from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    userprofile_id = serializers.IntegerField(source='UserProfile.id', read_only=True)
    avatar = serializers.ImageField(source='UserProfile.avatar', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', 'userprofile_id']
