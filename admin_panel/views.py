from django.shortcuts import render

from blog.models import UserProfile


class AdminHome:
    def home(self):
        user_profile = UserProfile.objects.get(user=self.user)
        return render(self, 'admin_panel/dashboard.html', {'user_profile': user_profile})


class User:
    def info(self):
        user_profile = UserProfile.objects.get(user=self.user)
        return render(self, 'admin_panel/user_info.html', {'user_profile': user_profile})
