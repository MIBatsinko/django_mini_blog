from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse, path, include
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase, APIRequestFactory, APIClient

from article.models import Article, Category
from blog import views as blog_views
from blog.views import ArticleDetailView, ArticleUpdateView, ArticleDeleteView
from my_account import views as account_views
from comment import views as comment_views


class ArticleTests(APITestCase, URLPatternsTestCase):
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

        path('<int:article>/', comment_views.CommentsDetailView.as_view(), name='comments_view'),
        path('<int:pk>/edit', comment_views.CommentUpdateView.as_view(), name='comment_edit'),
        path('<int:pk>/delete', comment_views.CommentDeleteView.as_view(), name='comment_delete'),
        path('<int:article_id>/comment_add/', comment_views.CommentCreateView.as_view(), name='comment_add'),
    ]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.category = Category.objects.create(name='test_cat', description='test123')
        self.client.login(username='john', password='johnpassword')
        self.url = reverse('blog_add')
        self.data = {
            'title': 'test title',
            'description': 'desc',
            'body': 'some body',
            'author': self.user.id,
            'category': self.category.id,
        }
        self.add_article = self.client.post(self.url, self.data, format='json', follow=True)

    def test_valid_create_article(self):
        # response = self.client.post(self.url, self.data, format='json', follow=True)
        self.assertEqual(self.add_article.status_code, 200)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().title, 'test title')

    def test_invalid_create_article(self):
        data = {
            'title': 'invalid article',
            'description': '',  # empty
            'body': 'some body',
            'author': self.user.id,
            'category': self.category.id,
        }

        self.client.post(self.url, data, format='json', follow=True)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get(id=1).title, 'test title')

    def test_view_articles(self):
        url = reverse('blog_index')
        response = self.client.get(url, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.context['blog']
        self.assertEqual(len(data), 1)  # AttributeError: 'HttpResponse' object has no attribute 'data'

    def test_check_response_data(self):
        response = self.client.get('/1/')
        data = {
            'id': response.context_data['view'].request.user.id,
            'username': response.context_data['view'].request.user.username,
        }
        self.assertEqual(data, {'id': 1, 'username': 'john'})

    def test_rendering_responses(self):
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

    def test_delete_article(self):
        response_data = Article.objects.all()
        print("Created: ", response_data)
        self.assertEqual(len(response_data), 1)

        factory = APIRequestFactory(enforce_csrf_checks=True)
        view = ArticleDeleteView.as_view()
        request = factory.delete('/1/')
        view(request, pk='1')
        response_data = Article.objects.all()
        print("Deleted: ", response_data)
        self.assertEqual(len(response_data), 0)

    def test_update_article(self):
        data = {
            'title': 'remember to email dave',
            'description': 'desc',
            'body': 'some body',
        }
        print("Articles: ", Article.objects.get(id=1))

        from django.test.client import encode_multipart
        factory = APIRequestFactory(enforce_csrf_checks=True)
        content = encode_multipart('BoUnDaRyStRiNg', data)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        view = ArticleUpdateView.as_view()
        request = factory.put(f'{1}/update/', content, content_type=content_type)
        response = view(request, pk='1')
        response.render()
        print(response.context_data)
        print(response.context_data['form'].errors)

        # print("DATA: ", self.add_article.context.keys())
        url = reverse('blog_edit', kwargs={'pk': 1})
        # url = f'{1}/update/'
        response = self.client.put(url, data)

        # client = APIClient()
        # client.post(url, data, format='json')

        print("After update: ", Article.objects.all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().title, 'test title')
