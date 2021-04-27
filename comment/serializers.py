from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source='User.id', read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        # read_only_fields = ['article', 'author']

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


class LimitedCommentlistSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        comments_limit = 10
        data = data.all().order_by('-id')[:comments_limit]
        return super(LimitedCommentlistSerializer, self).to_representation(data)


class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = LimitedCommentlistSerializer
        model = Comment
        fields = ['id', 'body', 'date_created']
        read_only_fields = ['article', 'author']

    def to_representation(self, instance):
        rep = super(UserCommentSerializer, self).to_representation(instance)
        rep['article'] = {
            'id': instance.article.id,
            'title': instance.article.title,
            'description': instance.article.description,
            'body': instance.article.body,
        }
        return rep
