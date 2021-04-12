from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DeleteView, DetailView
from django.db import models

from article.forms import CategoriesForm
from article.models import Article, Category
from blog.forms import UserProfileForm, ArticlesForm, RatingForm
from blog.models import UserProfile, Rating
from comment.forms import CommentsForm
from comment.models import Comment
from sendemail.views import SendingEmail


class AdminHome:
    @login_required()
    def home(self):
        context = {

        }
        return render(self, 'admin_panel/dashboard.html', context)


class AdminUsers:
    @login_required()
    def show_all(self):
        """
        Prints on the page all users
        """
        users = UserProfile.objects.all()
        context = {
            'users': users
        }
        return render(self, 'admin_panel/users/users.html', context)


class AdminUserProfile:
    @login_required()
    def info(self, pk):
        """
        User profile settings page
        """
        userprofile_id = UserProfile.objects.get(user=pk)
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
            form = UserProfileForm()
        return render(self, 'admin_panel/users/user_info.html', {'form': form, 'user_profile': userprofile_id})

    @login_required()
    def edit(self, pk):
        """
        Edit user profile
        """
        user_profile = UserProfile.objects.get(user=pk)
        user = User.objects.get(id=pk)
        if self.method == "POST":
            form = UserProfileForm(self.POST, self.FILES, instance=user_profile)
            if form.is_valid():
                instance = form.save(commit=False)
                is_staff = self.POST.get("is_staff", False)
                is_active = self.POST.get("is_active", False)
                is_superuser = self.POST.get("is_superuser", False)
                user_profile.user.is_staff = is_staff
                user_profile.user.is_active = is_active
                user_profile.user.is_superuser = is_superuser
                # user_profile.user.username = username
                user_profile.user.save()
                instance.name = self.POST['name']
                instance.email = self.POST['email']
                if self.FILES:
                    instance.avatar = self.FILES['avatar']
                instance.save()
        else:
            form = UserProfileForm()

        check_active = ''
        check_staff = ''
        check_super = ''
        if user_profile.user.is_staff:
            check_staff = 'checked'
        if user_profile.user.is_active:
            check_active = 'checked'
        if user_profile.user.is_superuser:
            check_super = 'checked'

        data = {
            'form': form,
            'error': form.errors,
            'user_profile': user_profile,
            'check_staff': check_staff,
            'check_active': check_active,
            'check_super': check_super
        }
        return render(self, 'admin_panel/users/user_edit.html', data)


class AdminUsersDeleteView(DeleteView):
    model = User
    success_url = '/admin_panel/users/'
    template_name = 'admin_panel/users/user_delete.html'

    def get_context_data(self, **kwargs):
        context = super(AdminUsersDeleteView, self).get_context_data(**kwargs)
        context['user_profile'] = UserProfile.objects.all()
        return context


class AdminArticles:
    @login_required()
    def show_all(self):
        """
        Prints on the page all articles
        """
        articles = Article.objects.order_by('-date')
        context = {
            'articles': articles
        }
        return render(self, 'admin_panel/articles/articles.html', context)

    @login_required()
    def add(self):
        """
        Create a new article
        """
        message = 'Add new article'
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
            'form': form,
            'error': form.errors,
            'message': message,
        }
        return render(self, 'admin_panel/articles/article_add.html', data)


class AdminArticleDetailView(DetailView):
    model = Article
    template_name = 'admin_panel/articles/article_details.html'
    context_object_name = 'article'

    def get_queryset(self):
        articles = Article.objects.filter().annotate(
            rating_user=models.Count("ratings",
                                     filter=models.Q(ratings__user=self.request.user.id))
        ).annotate(
            middle_star=(models.Avg("ratings__star"))
        )
        return articles

    def get_context_data(self, **kwargs):
        context = super(AdminArticleDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        context['star_form'] = RatingForm()
        try:
            context['mark'] = Rating.objects.get(user=self.request.user.id, article=kwargs['object'].id)
        except Rating.DoesNotExist:
            context['mark'] = 0
        return context


class AdminArticleUpdateView(UpdateView):
    model = Article
    template_name = 'admin_panel/articles/article_edit.html'
    form_class = ArticlesForm
    success_url = '/admin_panel/articles/'


class AdminArticleDeleteView(DeleteView):
    model = Article
    success_url = '/admin_panel/articles/'
    template_name = 'admin_panel/articles/article_delete.html'


class AdminCategories:
    @login_required()
    def show_all(self):
        """
        Prints on the page all categories
        """
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(self, 'admin_panel/categories/categories.html', context)

    @login_required()
    def add(self):
        """
        Create a new category
        """
        message = 'Add new category'
        if self.method == "POST":
            form = CategoriesForm(self.POST)
            if form.is_valid():
                form.save()
                message = 'New category added!'
        else:
            form = CategoriesForm()

        data = {
            'form': form,
            'error': form.errors,
            'message': message,
        }
        return render(self, 'admin_panel/categories/category_add.html', data)


class AdminCategoryUpdateView(UpdateView):
    model = Category
    template_name = 'admin_panel/categories/category_edit.html'
    form_class = CategoriesForm
    success_url = '/admin_panel/categories/'


class AdminCategoryDeleteView(DeleteView):
    model = Category
    success_url = '/admin_panel/categories/'
    template_name = 'admin_panel/categories/category_delete.html'


class AdminCommentUpdateView(UpdateView):
    model = Comment
    template_name = 'admin_panel/comments/comment_add.html'
    form_class = CommentsForm
    success_url = '/admin_panel/articles/'


class AdminCommentDeleteView(DeleteView):
    model = Comment
    success_url = '/admin_panel/articles/'
    template_name = 'admin_panel/comments/comment_delete.html'


class AdminCommentNew:
    @login_required()
    def add(self, article_id):
        if self.method == "POST":
            form = CommentsForm(self.POST)
            if form.is_valid():
                author = User.objects.get(id=self.user.id)
                article = Article.objects.get(id=article_id)
                instance = form.save(commit=False)
                instance.article = article
                instance.author = author
                instance.save()

                email = SendingEmail()
                email.new_comment(article, author, instance.body)
                return redirect('/admin_panel/articles/details/{}/'.format(article.id))
        else:
            form = CommentsForm()

        data = {
            'form': form,
            'error': form.errors,
        }

        return render(self, 'admin_panel/comments/comment_add.html', data)
