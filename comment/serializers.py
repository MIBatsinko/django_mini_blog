from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.Serializer):
    body = serializers.CharField()
    article_id = serializers.IntegerField()
    author_id = serializers.IntegerField()

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.article_id = validated_data.get('article_id', instance.article_id)
        instance.author_id = validated_data.get('author_id', instance.author_id)

        instance.save()
        return instance
