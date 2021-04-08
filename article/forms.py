from django.forms import ModelForm, TextInput, Textarea, ModelChoiceField, RadioSelect

from article.models import Category


class CategoriesForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
