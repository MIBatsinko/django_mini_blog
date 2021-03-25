from .models import Comment
from django.forms import ModelForm, Textarea, TextInput, HiddenInput


class CommentsForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']#, 'article', 'author']

        widgets = {
            'body': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment'
            }),
            # 'article': HiddenInput(),
            # 'author': HiddenInput(),
        }
