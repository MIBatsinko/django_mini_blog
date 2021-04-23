from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source='User.id', read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['author_id']

    def to_representation(self, instance):
        rep = super(CommentSerializer, self).to_representation(instance)
        rep['author'] = {
            'id': instance.author.id,
            'username': instance.author.username,
            'name': instance.author.first_name,
            'email': instance.author.email,
            'date of register': instance.author.date_joined,
            'avatar': instance.author.userprofile.avatar.url,
        }
        rep['article'] = {
            'id': instance.article.id,
            'title': instance.article.title,
            'description': instance.article.description,
            'body': instance.article.body,
        }
        return rep

        # def create(self, validated_data):
        #
        #     return Comment.objects.create(**validated_data)
        #
        # def update(self, instance, validated_data):
        #     instance.text = validated_data.get('text', instance.text)
        #     instance.location = validated_data.get('location', instance.location)
        #     instance.save()
        #     return instance