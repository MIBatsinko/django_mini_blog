from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.views.generic import DetailView, UpdateView, DeleteView
from django.views.generic.detail import BaseDetailView

from article.models import Article
from comment.models import Comment
from .forms import ArticlesForm, UserProfileForm, RatingForm
from .models import UserProfile, Rating


class BlogHomePage:
    def home(self):
        blog = Article.objects.all()

        # num_authors = Author.objects.count()  # The 'all()' is implied by default.
        # user = User.objects.get()
        # Number of visits to this view, as counted in the session variable.
        num_visits = self.session.get('num_visits', 0)
        self.session['num_visits'] = num_visits + 1

        return render(self, 'blog/blog_index.html', {"blog": blog, 'num_visits': num_visits})


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/blog_view.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        context['star_form'] = RatingForm()
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
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("article")),
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
        error = ''
        if self.method == "POST":
            form = ArticlesForm(self.POST)
            if form.is_valid():
                author_id = User.objects.get(id=self.user.id)
                instance = form.save(commit=False)
                instance.author = author_id
                instance.save()
                return redirect('blog_index')
            else:
                error = "Invalid form"

        form = ArticlesForm()

        data = {
            'form': form,
            'error': error,
        }
        return render(self, 'blog/blog_add.html', data)


class UserProfilePage:
    def profile(self, username, user_id):
        """
        User profile page
        """
        user = User.objects.get(username=username)
        if self.method == "GET":

            # Adds new UserProfile if it with the user_id does not exist
            try:
                user_profile = UserProfile.objects.get(user=user_id)
            except:
                user_profile = UserProfile.objects.create(user=user)

        user_profile = UserProfile.objects.get(user=user_id)

        data = {
            'user': user,
            'user_profile': user_profile,
        }
        return render(self, 'blog/profile.html', data)


class UserProfileSettings:
    def profile_settings(self, pk):
        """
        User profile settings page
        """
        userprofile_id = UserProfile.objects.get(user=pk)
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
