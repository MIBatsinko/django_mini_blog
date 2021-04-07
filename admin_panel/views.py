from django.shortcuts import render

from blog.models import UserProfile


class BlogHomePage:
    def home(self):
        user_profile = UserProfile.objects.get(user=self.user)
        return render(self, 'admin_panel/dashboard.html', {'user_profile': user_profile})
