from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea, ModelChoiceField, RadioSelect, CharField, PasswordInput, Form
from django.contrib.auth.models import User


class UserRegistrationForm(ModelForm):
    password = CharField(label='Password', widget=PasswordInput)
    password2 = CharField(label='Repeat password', widget=PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Passwords don\'t match.')
        return cd['password2']


class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)
