from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from admin_panel.forms import AdminUserInfoForm
from blog.forms import UserProfileForm
from blog.models import UserProfile


class AdminHome:
    def home(self):
        user_profile = UserProfile.objects.get(user=self.user)
        return render(self, 'admin_panel/dashboard.html', {'user_profile': user_profile})


class AdminUserProfile:
    def info(self):
        """
        User profile settings page
        """
        userprofile_id = UserProfile.objects.get(user=self.user.id)
        user_id = User.objects.get(username=userprofile_id)
        if self.method == 'POST':
            form = UserProfileForm(self.POST, self.FILES, instance=userprofile_id)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user_id
                if self.FILES:
                    instance.avatar = self.FILES['avatar']
                instance.name = self.POST['name']
                instance.email = self.POST['email']
                instance.save()
                return redirect('./')
        else:
            form = UserProfileForm(initial={
                'name': userprofile_id.name,
                'email': userprofile_id.email,
                'avatar': userprofile_id.avatar
            })
        print(form)
        return render(self, 'admin_panel/user_info.html', {'form': form, 'user_profile': userprofile_id})
