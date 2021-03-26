from article.models import Article  # , Author
from .models import UserProfile
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea, ValidationError
from django.core.files.images import get_image_dimensions


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


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        # fields = '__all__'
        exclude = ['user']
    #
    # def clean_avatar(self):
    #     avatar = self.cleaned_data['avatar']
    #     try:
    #         w, h = get_image_dimensions(avatar)
    #
    #         # validate dimensions
    #         max_width = max_height = 100
    #         if w > max_width or h > max_height:
    #             raise ValidationError(
    #                 u'Please use an image that is %s x %s pixels or smaller.' % (max_width, max_height))
    #
    #         # validate content type
    #         main, sub = avatar.content_type.split('/')
    #         if not (main == 'image' and sub in ['jpeg', 'jpg', 'gif', 'png']):
    #             raise ValidationError(u'Please use a JPEG, GIF or PNG image.')
    #
    #         # validate file size
    #         if len(avatar) > (20 * 1024):
    #             raise ValidationError(u'Avatar file size may not exceed 20k.')
    #
    #     except AttributeError:
    #         """
    #             Handles case when we are updating the user profile
    #             and do not supply a new avatar
    #             """
    #         pass
    #
    #     return avatar
