from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from admin_panel.forms import AdminUserInfoForm
from article.models import Article
from blog.forms import UserProfileForm, ArticlesForm
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


class AdminArticles:
    def show_all(self):
        """
        Show all articles
        """
        user_profile = UserProfile.objects.get(user=self.user)
        articles = Article.objects.order_by('-date')
        context = {
            'user_profile': user_profile,
            'articles': articles
        }
        return render(self, 'admin_panel/articles.html', context)

    def add(self):
        """
        Create a new article
        """
        message = 'Add new article'
        user_profile = UserProfile.objects.get(user=self.user)
        if self.method == "POST":
            form = ArticlesForm(self.POST)
            if form.is_valid():
                author_id = User.objects.get(id=self.user.id)
                instance = form.save(commit=False)
                instance.author = author_id
                instance.save()
                message = 'Article {} added!'.format(instance.title)
        else:
            form = ArticlesForm()

        data = {
            'user_profile': user_profile,
            'form': form,
            'error': form.errors,
            'message': message,
        }
        return render(self, 'admin_panel/article_add.html', data)

    def edit(self):
        """
        Edit article
        """
        pass

    def delete(self):
        """
        Delete article
        """
        pass
