from django.contrib.auth.models import User
from rest_framework import serializers

from article.models import Article
from users.models import UserProfile
from comment.serializers import UserCommentSerializer


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='User.userprofile.avatar', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'avatar', 'userprofile']
        read_only_fields = ['userprofile']

    def to_representation(self, instance):
        rep = super(UserSerializer, self).to_representation(instance)
        rep['avatar'] = instance.userprofile.avatar.url
        return rep


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='userprofile.avatar')

    class Meta:
        model = UserProfile
        fields = ['id', 'avatar']


class UserResponseSerializer(UserSerializer):
    userprofile = UserProfileSerializer()


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
    avatar = serializers.ImageField(source='userprofile.avatar')
    userprofile_id = serializers.IntegerField(source='userprofile.id', read_only=True)
    total_rating = serializers.FloatField(source='userprofile.total_rating', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'comments', 'articles', 'userprofile_id',
                  'total_rating', 'avatar']

    def update(self, instance, validated_data):
        userprofile_data = validated_data.pop('userprofile')
        profile = instance.userprofile

        instance.id = validated_data.get('id', instance.id)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.avatar = userprofile_data.get('avatar', profile.avatar)
        profile.save()
        return instance
