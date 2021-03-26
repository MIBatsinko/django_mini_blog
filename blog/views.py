from PIL import Image
from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from article.models import Article  # , Author
from django.contrib.auth.models import User
from comment.models import Comment
from .forms import ArticlesForm, UserProfileForm
from django.views.generic import DetailView, UpdateView, DeleteView

from .models import UserProfile


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
        ctx = super(NewsDetailView, self).get_context_data(**kwargs)
        ctx['comments'] = Comment.objects.all()
        return ctx


class NewsUpdateView(UpdateView):
    model = Article
    template_name = 'blog/blog_add.html'

    form_class = ArticlesForm


class NewsDeleteView(DeleteView):
    model = Article
    success_url = '/blog/'
    template_name = 'blog/blog_delete.html'


def create(request):
    """
    Create a new article
    """
    error = ''
    if request.method == "POST":
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
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


def profile_settings(request):
    """
    User profile settings page
    """
    user_id = User.objects.get(username='first_user')
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_id)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'blog/profile_settings.html', context)


def upload_pic(request):
    if request.method == 'POST':
        layout = UserProfile()
        layout.image = "/static/images/avatar.png"
        layout.save()

    # form = UserProfileForm(request.POST, request.FILES, instance=request.user)
    # # Выбор картинки
    # img = Image.open(self.avatar.path)
    # # Условие
    # if img.height > 300 or img.width > 300:
    #     output_size = (300, 300)
    #     img.thumbnail(output_size)
    #     img.save('/WOW/img.png')
    #     print('save')
    # print('no')


def useravatar(request, user_id):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            av = User.objects.get(user_id=user_id)
            av.avatar = request.FILES['avatar']
            # other columns if you want to save, same as above line, except request.FILES will be request.POST['input_name']
            av.save()
            # messages.success(request, 'Your avatar was successfully Uploaded!')
            return redirect('', user_pk=request.user.pk)

# def upload_pic(request, user_id):
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             m = UserProfile.objects.get(user=user_id)
#             m.avatar = form.cleaned_data['image']
#             m.save()
#             return HttpResponse('image upload success')
#     return HttpResponseForbidden('allowed only via POST')
