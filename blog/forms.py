from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, Textarea, ModelChoiceField, RadioSelect

from article.models import Article, Category
from .models import UserProfile, Rating, RatingStar


class ArticlesForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'description', 'body']

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
        }


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user', 'total_rating']


# class UserProfileForm(ModelForm):
#     class Meta:
#         model = UserProfile
#         # exclude = ['user', 'total_rating']
#         fields = ['avatar']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name']  # , 'is_active', 'is_staff', 'is_superuser']


class RatingForm(ModelForm):
    star = ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)
