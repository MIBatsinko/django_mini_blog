from copy import deepcopy

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.views.generic import DetailView, UpdateView, DeleteView
from django.db import models

from article.models import Article
from comment.models import Comment
from .forms import ArticlesForm, UserProfileForm, RatingForm
from .models import UserProfile, Rating


class BlogHomePage:
    def home(self):
        blog = Article.objects.all()

        # num_authors = Author.objects.count()  # The 'all()' is implied by default.
        # Number of visits to this view, as counted in the session variable.
        num_visits = self.session.get('num_visits', 0)
        self.session['num_visits'] = num_visits + 1

        return render(self, 'blog/blog_index.html', {"blog": blog, 'num_visits': num_visits})


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/blog_view.html'
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
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        context['star_form'] = RatingForm()
        try:
            context['mark'] = Rating.objects.get(user=self.request.user.id, article=kwargs['object'].id)
        except Rating.DoesNotExist:
            context['mark'] = 0
        return context


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'blog/blog_add.html'

    form_class = ArticlesForm


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = '/'
    template_name = 'blog/blog_delete.html'


class AddStarRating(View):
    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                article_id=int(request.POST.get("article")),
                user=User.objects.get(id=request.user.id),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class ArticleAdd:
    def create(self):
        """
        Create a new article
        """
        if self.method == "POST":
            form = ArticlesForm(self.POST)
            if form.is_valid():
                author_id = User.objects.get(id=self.user.id)
                instance = form.save(commit=False)
                instance.author = author_id
                instance.save()
                return redirect('blog_index')
        else:
            form = ArticlesForm()

        data = {
            'form': form,
            'error': form.errors,
        }
        return render(self, 'blog/blog_add.html', data)


class UserProfilePage:
    def profile(self, username):
        """
        User profile page
        """
        user = User.objects.get(username=username)
        if self.method == "GET":

            # Adds new UserProfile if it with the user_id does not exist
            try:
                user_profile = UserProfile.objects.get(user=self.user.id)
            except:
                user_profile = UserProfile.objects.create(user=user)

        user_profile = UserProfile.objects.get(user=self.user.id)

        data = {
            'user': user,
            'user_profile': user_profile,
        }
        return render(self, 'blog/profile.html', data)


class UserProfileSettings:
    def profile_settings(self):
        """
        User profile settings page
        """
        userprofile_id = UserProfile.objects.get(user=self.user.id)
        user_id = User.objects.get(username=userprofile_id)
        form = UserProfileForm()
        if self.method == 'POST':
            form = UserProfileForm(self.POST, self.FILES, instance=userprofile_id)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user_id
                instance.avatar = self.FILES['avatar']
                instance.name = self.POST['name']
                instance.email = self.POST['email']
                instance.save()
                return redirect('blog_index')
        context = {'form': form}
        return render(self, 'blog/profile_settings.html', context)


class RatingUserPage:
    def show_rating(self, **kwargs):
        users_rating = Rating.objects.raw("SELECT id, article_id, AVG(star_id) as avg, (SELECT author_id from article_article WHERE blog_rating.article_id = article_article.id) as author FROM blog_rating GROUP BY article_id")

        data_rating = dict()
        for i in users_rating:
            data_rating[i.article_id] = {'article_id': i.article_id,
                                         'avg_star': i.avg,
                                         'author': i.author}
        print(data_rating)
        return render(self, 'blog/user_rating.html', data_rating)
