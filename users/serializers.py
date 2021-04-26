from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from blog.models import UserProfile
from comment.models import Comment
from comment.serializers import CommentSerializer, UserCommentSerializer


class UserSerializer(serializers.ModelSerializer):
    # userprofile_id = serializers.IntegerField(source='UserProfile.id', read_only=True)
    avatar = serializers.ImageField(source='UserProfile.avatar', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', 'userprofile']

    def to_representation(self, instance):
        rep = super(UserSerializer, self).to_representation(instance)
        rep['userprofile'] = {
            'id': instance.userprofile.id,
            'avatar': instance.userprofile.avatar.url,
        }
        return rep


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'avatar']


class UserResponseSerializer(UserSerializer):
    userprofile = UserProfileSerializer()
    comments = CommentSerializer()


class SingleUserSerializer(serializers.ModelSerializer):
    # userprofile_id = serializers.IntegerField(source='UserProfile.id', read_only=True)
    # avatar = serializers.ImageField(source='UserProfile.avatar', read_only=True)
    comments = UserCommentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'comments']  # , 'userprofile']

    def to_representation(self, instance):
        rep = super(SingleUserSerializer, self).to_representation(instance)
        rep['userprofile'] = {
            'id': instance.userprofile.id,
            'avatar': instance.userprofile.avatar.url,
            'total rating': instance.userprofile.total_rating
        }
        # rep['comments'] = instance.comments.all()
        return rep
