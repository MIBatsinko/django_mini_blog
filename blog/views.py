from copy import deepcopy

from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic.base import View, TemplateView
from django.contrib.auth.models import User
from django.views.generic import DetailView, UpdateView, DeleteView, FormView
from django.db import models
from rest_framework.generics import get_object_or_404

from article.models import Article, Category
from comment.models import Comment
from .forms import ArticlesForm, UserProfileForm, RatingForm, UserForm
from .models import UserProfile, Rating


class BlogHomePage:
    def home(self):
        blog = Article.objects.order_by('-date')
        categories = Category.objects.all()

        # num_authors = Author.objects.count()  # The 'all()' is implied by default.
        # Number of visits to this view, as counted in the session variable.
        num_visits = self.session.get('num_visits', 0)
        self.session['num_visits'] = num_visits + 1

        return render(self, 'blog/blog_index.html', {"blog": blog, 'categories': categories, 'num_visits': num_visits})


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


# class UserProfilePage:
#     def profile(self):
#         """
#         User profile page
#         """
#         # Adds new UserProfile if it with the user_id does not exist
#         # try:
#         #     user_profile = UserProfile.objects.get(user=self.user)
#         # except:
#         #     user_profile = UserProfile.objects.create(user=user)
#
#         data = {
#             'user': self.user,
#         }
#         return render(self, 'blog/profile.html', data)


class UserProfilePageView(TemplateView):
    model = UserProfile
    template_name = 'blog/profile.html'
    context_object_name = 'userprofile'


# class UserProfileSettings:
#     def profile_settings(self):
#         """
#         User profile settings page
#         """
#         userprofile = UserProfile.objects.get(user=self.user.id)
#         user = User.objects.get(id=self.user.id)
#         user_profile_form = UserProfileForm(initial={
#             'avatar': userprofile.avatar
#         })
#         user_form = UserForm(initial={
#             'name': userprofile.user.first_name,
#             'email': userprofile.user.email
#         })
#         if self.method == 'POST':
#             user_profile_form = UserProfileForm(self.POST, self.FILES, instance=userprofile)
#             user_form = UserForm(self.POST, self.FILES, instance=user)
#             if user_form.is_valid():
#                 instance = user_form.save(commit=False)
#                 instance.user = user
#                 instance.first_name = self.POST['first_name']
#                 instance.email = self.POST['email']
#                 instance.save()
#                 return redirect('profile')
#         context = {'form': user_form}
#         return render(self, 'blog/profile_settings.html', context)


# дві форми. UserProfileSettings працює
# class UserProfileUpdateView(UpdateView):
#     model = UserProfile
#     template_name = 'blog/profile_settings.html'
#     context_object_name = 'userprofile'
#
#     form_class = UserProfileForm
#
#     def form_valid(self, form):
#         form = UserForm(self.request.POST, instance=self.request.user)
#         form.save()
#         return render(self.request, 'discussion.html', context={
#             'form': form,
#             # 'formset': formset
#         })
#
#     def get_object(self, **kwargs):
#         return get_object_or_404(User, pk=self.request.user.id)


class UserProfileUpdateView(UpdateView):
    template_name = 'blog/profile_settings.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        user_profile_form = UserProfileForm(initial={
                'avatar': user.userprofile.avatar,
            })
        user_profile_form.prefix = 'user_profile_form'
        user_form = UserForm(initial={
                'first_name': user.first_name,
                'email': user.email
            })
        user_form.prefix = 'user_form'
        # Use RequestContext instead of render_to_response from 3.0
        context = {'user_profile_form': user_profile_form, 'user_form': user_form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user.username)
        user_profile_form = UserProfileForm(self.request.POST, self.request.FILES,
                                            instance=user.userprofile, prefix='user_profile_form')
        user_form = UserForm(self.request.POST, prefix='user_form', instance=user)
        if user_profile_form.is_valid() and user_form.is_valid():
            instance = user_form.save(commit=False)
            instance.save()
            user_profile_form.save()
            return redirect('profile')


# class RatingUserPage:
#     def show_rating(self, **kwargs):
#         data_rating = UserProfile.objects.all()
#         return render(self, 'blog/user_rating.html', {'data_rating': data_rating})


class RatingUserPageView(TemplateView):
    model = User
    template_name = 'blog/user_rating.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super(RatingUserPageView, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context
