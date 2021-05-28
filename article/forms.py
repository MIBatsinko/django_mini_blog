from django.forms import ModelForm

from article.models import Category


class CategoriesForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
