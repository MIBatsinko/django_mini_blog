from my_account.forms import UserRegistrationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from my_account.forms import LoginForm
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout


class LoginView(View):
    def post(self, request):
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
                return render(request, 'my_account/page-login.html', {'error': "Invalid login!", 'form': form})
        else:
            return render(request, 'my_account/page-login.html', {'form': form})

    def get(self, request):
        form = LoginForm()
        return render(request, 'my_account/page-login.html', {'form': form})


class SignupView(View):
    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            return render(request, 'my_account/register_done.html', {'new_user': new_user})
        return render(request, 'my_account/page-sign-up.html', {'user_form': user_form})

    def get(self, request):
        user_form = UserRegistrationForm()
        return render(request, 'my_account/page-sign-up.html', {'user_form': user_form})

#
# def register(request):
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             # Create a new user object but avoid saving it yet
#             new_user = user_form.save(commit=False)
#             # Set the chosen password
#             new_user.set_password(user_form.cleaned_data['password'])
#             # Save the User object
#             new_user.save()
#             # Create a new profile
#             # user_profile = UserProfile.objects.create(user=new_user)
#
#             return render(request, 'my_account/register_done.html', {'new_user': new_user})
#     else:
#         user_form = UserRegistrationForm()
#     return render(request, 'my_account/page-sign-up.html', {'user_form': user_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")

