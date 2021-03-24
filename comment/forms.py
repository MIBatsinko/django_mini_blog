from .models import Comment
from django.forms import ModelForm, Textarea


class CommentsForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'author']

        widgets = {
            'body': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Post text'
            }),
            'author': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Post text'
            }),
        }
