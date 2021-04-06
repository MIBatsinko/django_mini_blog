from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    rating_user = serializers.BooleanField()
    middle_star = serializers.FloatField()

    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ['author', 'date']
