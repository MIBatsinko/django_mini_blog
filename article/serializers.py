from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Article, Category


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ['author', 'date', 'total_rating']

    def to_representation(self, instance):
        rep = super(ArticleSerializer, self).to_representation(instance)
        rep['author'] = {
            'id': instance.author.id,
            'username': instance.author.username,
            'name': instance.author.first_name,
            'email': instance.author.email,
            'date of register': instance.author.date_joined,
            'avatar': instance.author.userprofile.avatar.url,
        }
        rep['category'] = {
            'id': instance.category.id,
            'name': instance.category.name,
            'description': instance.category.description,
        }
        return rep


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ArticleResponseSerializer(ArticleSerializer):
    author = UserSerializer()
    category = CategorySerializer()
