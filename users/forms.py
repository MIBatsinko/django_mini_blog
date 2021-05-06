from django.contrib.auth.models import User
from django.forms import ModelForm

from users.models import UserProfile


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user', 'total_rating']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name']  # , 'is_active', 'is_staff', 'is_superuser']
