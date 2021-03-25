from article.models import Article  # , Author
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea


class ArticlesForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'description', 'body', 'author']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Post title'
            }),
            'description': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Post desc'
            }),
            'body': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Post text'
            }),
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Post author'
            }),
        }
