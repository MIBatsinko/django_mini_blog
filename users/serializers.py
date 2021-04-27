from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

# from article.serializers import UserArticleSerializer
from article.models import Article
from blog.models import UserProfile
from comment.models import Comment
from comment.serializers import CommentSerializer, UserCommentSerializer


class UserSerializer(serializers.ModelSerializer):
    # userprofile_id = serializers.IntegerField(source='UserProfile.id', read_only=True)
    avatar = serializers.ImageField(source='User.userprofile.avatar', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', 'userprofile']
        read_only_fields = ['userprofile']

    def to_representation(self, instance):
        rep = super(UserSerializer, self).to_representation(instance)
        # rep['userprofile_id'] = instance.userprofile.id
        rep['avatar'] = instance.userprofile.avatar.url
        return rep


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'avatar']


class UserResponseSerializer(UserSerializer):
    userprofile = UserProfileSerializer()
    # comments = CommentSerializer()


class LimitedArticlelistSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        articles_limit = 10
        data = data.all().order_by('-total_rating')[:articles_limit]
        return super(LimitedArticlelistSerializer, self).to_representation(data)


class UserArticleSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = LimitedArticlelistSerializer
        model = Article
        fields = ['id', 'title', 'body', 'description', 'total_rating']


class SingleUserSerializer(serializers.ModelSerializer):
    comments = UserCommentSerializer(many=True, read_only=True)
    articles = UserArticleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'comments', 'articles']  # , 'userprofile']

    def to_representation(self, instance):
        rep = super(SingleUserSerializer, self).to_representation(instance)
        rep['userprofile'] = {
            'id': instance.userprofile.id,
            'avatar': instance.userprofile.avatar.url,
            'total rating': instance.userprofile.total_rating
        }
        return rep
