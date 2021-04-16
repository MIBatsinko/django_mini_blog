from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.views import _ajax_response
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from blog.models import UserProfile
from .forms import UserRegistrationForm
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.http import HttpResponseRedirect
from django.views.generic.base import View, TemplateView
from django.contrib.auth import logout


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return HttpResponse('Disabled my_account')
            else:
                return render(request, 'my_account/invalid_login.html')
    else:
        form = LoginForm()
    return render(request, 'my_account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create a new profile
            user_profile = UserProfile.objects.create(user=new_user)

            return render(request, 'my_account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'my_account/register.html', {'user_form': user_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")
