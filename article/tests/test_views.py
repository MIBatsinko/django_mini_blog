from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse, path, include
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase, APIRequestFactory, APIClient
from rest_framework.utils import json

from article.models import Article, Category
from blog import views as blog_views
from blog.views import ArticleDetailView, ArticleUpdateView, ArticleDeleteView
from my_account import views as account_views
from comment import views as comment_views


class ArticleTests(APITestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.category = Category.objects.create(name='test_cat', description='test123')
        self.client.login(username='john', password='johnpassword')
        self.url = reverse('blog_add')
        self.data = {
            'title': 'test_title',
            'description': 'desc',
            'body': 'some_body',
            'author': self.user.id,
            'category': self.category.name,
        }
        self.add_article = self.client.post(self.url, self.data, format='json', follow=True)

    def test_valid_create_article(self):
        self.assertEqual(self.add_article.status_code, 200)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().title, 'test_title')

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

    def test_view_articles(self):
        url = reverse('blog_index')
        response = self.client.get(url, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.context['blog']
        self.assertEqual(len(data), 1)

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
        self.assertEqual(data, {"id": 1, "title": "test_title"})

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
        update_url = reverse('blog_edit', kwargs={'pk': 1})

        # GET the form
        response = self.client.get(update_url)

        # retrieve form data as dict
        form = response.context['form']
        data = form.initial  # form is unbound but contains data
        print("Before update: ", Article.objects.get(id=1).title, Article.objects.get(id=1).description, Article.objects.get(id=1).body)
        # manipulate some data
        data['title'] = 'updated_value'

        # POST to the form
        response = self.client.post(update_url, data)

        # retrieve again
        response = self.client.get(update_url)
        print("After update: ",
              Article.objects.get(id=1).title,
              Article.objects.get(id=1).description,
              Article.objects.get(id=1).body)

        self.assertContains(response, 'updated_value')  # or
        self.assertEqual(response.context['form'].initial['title'], 'updated_value')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().title, 'updated_value')
