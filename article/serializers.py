from rest_framework import serializers

from users.serializers import UserSerializer
from article.models import Article, Category


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
            'first name': instance.author.first_name,
            'last name': instance.author.last_name,
            'rating': instance.author.userprofile.total_rating,
            'email': instance.author.email,
            'date of register': instance.author.date_joined,
        }
        try:
            rep['author']['avatar'] = instance.author.userprofile.avatar.url,
        except ValueError:
            rep['author']['avatar'] = "/media/avatar.png",

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



