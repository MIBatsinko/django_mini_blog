from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.views.generic import DetailView, UpdateView, DeleteView

from article.models import Article
from comment.models import Comment
from .forms import ArticlesForm, UserProfileForm, RatingForm
from .models import UserProfile, Rating


def news_home(request):
    blog = Article.objects.all()

    # num_authors = Author.objects.count()  # The 'all()' is implied by default.
    # user = User.objects.get()
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(request, 'blog/blog_index.html', {"blog": blog, 'num_visits': num_visits})


class NewsDetailView(DetailView):
    model = Article
    template_name = 'blog/blog_view.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        context['star_form'] = RatingForm()
        return context


class NewsUpdateView(UpdateView):
    model = Article
    template_name = 'blog/blog_add.html'

    form_class = ArticlesForm


class NewsDeleteView(DeleteView):
    model = Article
    success_url = '/blog/'
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


def create(request):
    """
    Create a new article
    """
    error = ''
    if request.method == "POST":
        form = ArticlesForm(request.POST)
        if form.is_valid():
            author_id = User.objects.get(id=request.user.id)
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
    return render(request, 'blog/blog_add.html', data)


def profile(request, username, user_id):
    """
    User profile page
    """
    user = User.objects.get(username=username)
    if request.method == "GET":

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
    return render(request, 'blog/profile.html', data)


def profile_settings(request, pk):
    """
    User profile settings page
    """
    userprofile_id = UserProfile.objects.get(user=pk)
    user_id = User.objects.get(username=userprofile_id)
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile_id)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user_id
            instance.avatar = request.FILES['avatar']
            instance.name = request.POST['name']
            instance.email = request.POST['email']
            instance.save()
            return redirect('blog_index')
    context = {'form': form}
    return render(request, 'blog/profile_settings.html', context)
