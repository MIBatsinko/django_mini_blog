from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse, path, include
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase, APIRequestFactory

from article.models import Article, Category
from blog import views as blog_views
from blog.views import ArticleDetailView
from my_account import views as account_views
from comment import views as comment_views


class ArticleTests(APITestCase, URLPatternsTestCase):
    # user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    category = Category.objects.create(name='test_cat', description='test123')
    from allauth.account import views as allauth_views
    urlpatterns = [
        path('', blog_views.BlogHomePage.home, name='blog_index'),
        path('add_post/', blog_views.ArticleCreateView.as_view(), name='blog_add'),
        path('<int:pk>/', blog_views.ArticleDetailView.as_view(), name='blog_view'),
        path('<int:pk>/update/', blog_views.ArticleUpdateView.as_view(), name='blog_edit'),
        path('<int:pk>/delete/', blog_views.ArticleDeleteView.as_view(), name='blog_delete'),
        path("add-rating/", blog_views.AddStarRating.as_view(), name='add_rating'),

        path("rating_user/", blog_views.RatingUserPageView.as_view(), name='rating_user'),
        path('profile/', blog_views.UserProfilePageView.as_view(), name='profile'),
        path('profile_settings/', blog_views.UserProfileUpdateView.as_view(), name="profile_settings"),
        path('login/', account_views.user_login, name='my_account_login'),
        path('register/', account_views.register, name='my_account_signup'),
        path('logout/', account_views.LogoutView.as_view(), name='my_account_logout'),
        path('password_reset/', allauth_views.PasswordResetView.as_view(), name='my_account_reset_password'),
        path('password_reset_done/', allauth_views.PasswordResetDoneView.as_view(),
             name='my_account_password_reset_done'),
        path('password_reset_from_key/', allauth_views.PasswordResetFromKeyView.as_view(),
             name='my_account_password_reset_from_key'),
        path('password_reset_from_key_done/', allauth_views.PasswordResetFromKeyDoneView.as_view(),
             name='my_account_password_reset_from_key_done'),
        path('password_set/', allauth_views.PasswordSetView.as_view(), name='my_account_password_set'),
        path('<int:article>/', comment_views.CommentsDetailView.as_view(), name='comments_view'),
        path('<int:pk>/edit', comment_views.CommentUpdateView.as_view(), name='comment_edit'),
        path('<int:pk>/delete', comment_views.CommentDeleteView.as_view(), name='comment_delete'),
        path('<int:article_id>/comment_add/', comment_views.CommentCreateView.as_view(), name='comment_add'),
    ]

    def test_create_article(self):
        """
        Ensure we can create a new account object.
        """
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.category = Category.objects.create(name='test_cat', description='test123')
        self.client.login(username='john', password='johnpassword')
        url = reverse('blog_add')
        data = {
            'title': 'test title',
            'description': 'desc',
            'body': 'some body',
            'author': self.user.id,
            'category': self.category.id,
        }
        response = self.client.post(url, data, format='json', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().title, 'test title')

    def test_view_articles(self):
        """
        Ensure we can create a new account object.
        """
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        url = reverse('blog_index')
        response = self.client.get(url, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 1)  # AttributeError: 'HttpResponse' object has no attribute 'data'

    def test_check_response_data(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.category = Category.objects.create(name='test_cat', description='test123')
        self.client.login(username='john', password='johnpassword')
        # print(User.objects.all())
        url = reverse('blog_add')
        data = {
            'title': 'test title',
            'description': 'desc',
            'body': 'some body',
            'author': self.user.id,
            'category': self.category.id,
        }
        response = self.client.post(url, data, format='json', follow=True)
        self.assertEqual(response.status_code, 200)
        # print('Article: ', Article.objects.get(id=1))
        response = self.client.get('/1/')
        data = {
            'id': response.context_data['view'].request.user.id,
            'username': response.context_data['view'].request.user.username,
        }
        # data = response.context_data
        # print(data)
        self.assertEqual(data, {'id': 1, 'username': 'john'})

    def test_rendering_responses(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.category = Category.objects.create(name='test_cat', description='test123')
        self.client.login(username='john', password='johnpassword')
        # print(User.objects.all())
        url = reverse('blog_add')
        data = {
            'title': 'test title',
            'description': 'desc',
            'body': 'some body',
            'author': self.user.id,
            'category': self.category.id,
        }
        response = self.client.post(url, data, format='json', follow=True)

        factory = APIRequestFactory(enforce_csrf_checks=True)
        view = ArticleDetailView.as_view()
        request = factory.get('/1/')
        response = view(request, pk='1')
        response.render()  # Cannot access `response.content` without this.
        data = {
            'id': response.context_data['article'].id,
            'title': response.context_data['article'].title,
        }
        # print(response.context_data['view'].request.GET)
        self.assertEqual(data, {"id": 1, "title": "test title"})
