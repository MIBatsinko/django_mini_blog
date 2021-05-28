from comment.models import Comment
from django.forms import ModelForm, Textarea


class CommentsForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

        widgets = {
            'body': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment'
            }),
        }
