from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse, path, include
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase, APIRequestFactory, APIClient, force_authenticate
from rest_framework.utils import json

from article.models import Article, Category
from article.views import ArticleApiView, SingleArticleApiView, SingleCategoryApiView
from blog.models import UserProfile
from blog.views import ArticleDetailView, ArticleUpdateView, ArticleDeleteView
from comment.models import Comment

#
# class ArticleWebTests(APITestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
#         self.category = Category.objects.create(name='test_cat', description='test123')
#         self.client.login(username='john', password='johnpassword')
#         self.url = reverse('blog_add')
#         self.data = {
#             'title': 'test_title',
#             'description': 'desc',
#             'body': 'some_body',
#             'category': self.category.name,
#         }
#         self.add_article = self.client.post(self.url, self.data, format='json', follow=True)
#
#     def test_valid_create_article(self):
#         data = {
#             'title': 'new_valid_title',
#             'description': 'new_valid_desc',
#             'body': 'new_valid_body',
#             'category': self.category.name,
#         }
#         self.add_new_valid_article = self.client.post(self.url, data, format='json', follow=True)
#         self.assertEqual(self.add_new_valid_article.status_code, 200)
#         self.assertEqual(Article.objects.count(), 2)
#
#     def test_invalid_create_article(self):
#         data = {
#             'title': 'invalid article',
#             'description': '',  # empty
#             'body': 'some body',
#             'author': self.user.id,
#             'category': self.category.name,
#         }
#
#         self.client.post(self.url, data, format='json', follow=True)
#         self.assertEqual(Article.objects.count(), 1)
#
#     def test_view_articles(self):
#         url = reverse('blog_index')
#         response = self.client.get(url, format='json', follow=True)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         data = response.context['blog']
#         self.assertEqual(len(data), 1)
#
#     def test_check_response_data(self):
#         response = self.client.get('/1/')
#         data = {
#             'id': response.context_data['view'].request.user.id,
#             'username': response.context_data['view'].request.user.username,
#         }
#         self.assertEqual(data, {'id': 1, 'username': 'john'})
#
#     def test_rendering_responses(self):
#         factory = APIRequestFactory(enforce_csrf_checks=True)
#         view = ArticleDetailView.as_view()
#         request = factory.get(reverse('blog_index'))
#         response = view(request, pk='1')
#         response.render()  # Cannot access `response.content` without this.
#         data = {
#             'id': response.context_data['article'].id,
#             'title': response.context_data['article'].title,
#         }
#         # print(response.context_data['view'].request.GET)
#         self.assertEqual(data, {"id": 1, "title": "test_title"})
#
#     def test_delete_article(self):
#         response_data = Article.objects.all()
#         print("Created: ", response_data)
#         self.assertEqual(len(response_data), 1)
#
#         factory = APIRequestFactory(enforce_csrf_checks=True)
#         view = ArticleDeleteView.as_view()
#         request = factory.delete(reverse('blog_delete', kwargs={'pk': 1}))
#         view(request, pk='1')
#         response_data = Article.objects.all()
#         print("Deleted: ", response_data)
#         self.assertEqual(len(response_data), 0)
#
#     def test_update_article(self):
#         update_url = reverse('blog_edit', kwargs={'pk': 1})
#
#         # GET the form
#         response = self.client.get(update_url)
#
#         # retrieve form data as dict
#         form = response.context['form']
#         data = form.initial  # form is unbound but contains data
#         print("Before update: ", Article.objects.get(id=1).title, Article.objects.get(id=1).description, Article.objects.get(id=1).body)
#         # manipulate some data
#         data['title'] = 'updated_value'
#
#         # POST to the form
#         response = self.client.post(update_url, data)
#
#         # retrieve again
#         response = self.client.get(update_url)
#         print("After update: ",
#               Article.objects.get(id=1).title,
#               Article.objects.get(id=1).description,
#               Article.objects.get(id=1).body)
#
#         self.assertContains(response, 'updated_value')  # or
#         self.assertEqual(response.context['form'].initial['title'], 'updated_value')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(Article.objects.count(), 1)
#         self.assertEqual(Article.objects.get().title, 'updated_value')
#
#
# class ArticleApiTests(APITestCase):
#     def setUp(self):
#         self.client = APIClient(enforce_csrf_checks=True)
#         self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
#         self.category = Category.objects.create(name='test_cat', description='test123')
#         self.client.force_authenticate(user=self.user)
#         # self.userprofile = UserProfile.objects.create(user=self.user)
#         # self.client.login(username='john', password='johnpassword')
#         self.url = reverse('view_articles')
#         self.data = {
#             'title': 'test_title',
#             'description': 'desc',
#             'body': 'some_body',
#             'category': self.category.id,
#         }
#         self.add_article = self.client.post(self.url, self.data, format='json', follow=True)
#
#     def test_valid_create_article(self):
#         valid_data = {
#             'title': 'new_valid_title',
#             'description': 'new_valid_desc',
#             'body': 'new_valid_body',
#             'category': self.category.id,
#         }
#
#         response = self.client.post(self.url, valid_data, format='json', follow=True)
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(Article.objects.count(), 2)
#         self.assertEqual(Article.objects.get(id=2).author, self.user)
#
#     def test_invalid_create_article(self):
#         invalid_data = {
#             'title': 'invalid article',
#             'description': '',  # empty
#             'body': 'some body',
#             'author': self.user.id,
#             'category': self.category.id,
#         }
#
#         self.client.post(self.url, invalid_data, format='json', follow=True)
#         self.assertEqual(Article.objects.count(), 1)
#
#     def test_view_articles(self):
#         url = reverse('view_articles')
#         response = self.client.get(url, format='json', follow=True)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Article.objects.count(), 1)
#
#     def test_check_response_data(self):
#         response = self.client.get(reverse('change_articles', kwargs={'pk': 1}), format='json')
#         response.render()
#         data = {
#             'id': json.loads(response.content)['id'],
#             'title': json.loads(response.content)['title']
#         }
#         self.assertEqual(data, {'id': 1, 'title': 'test_title'})
#
#     def test_rendering_responses(self):
#         factory = APIRequestFactory(enforce_csrf_checks=True)
#         view = ArticleDetailView.as_view()
#         request = factory.get(reverse('change_articles', kwargs={'pk': 1}))
#         response = view(request, pk='1')
#         response.render()
#         data = {
#             'id': response.context_data['article'].id,
#             'title': response.context_data['article'].title,
#         }
#         self.assertEqual(data, {"id": 1, "title": "test_title"})
#
#     def test_delete_article(self):
#         response_data = Article.objects.all()
#         print("Created: ", response_data)
#         self.assertEqual(len(response_data), 1)
#
#         factory = APIRequestFactory(enforce_csrf_checks=True)
#         view = SingleArticleApiView.as_view()
#         request = factory.delete(reverse('change_articles', kwargs={'pk': 1}))
#         view(request, pk='1')
#         response_data = Article.objects.all()
#         print("Deleted: ", response_data)
#         self.assertEqual(len(response_data), 0)
#
#     def test_update_article(self):
#         update_url = reverse('change_articles', kwargs={'pk': 1})
#
#         valid_data = {
#             'title': 'update_title',
#             'description': 'new_update_valid_desc',
#             'body': 'new_valupdate_id_body',
#             'category': self.category.id,
#         }
#         print(Article.objects.all())
#         response = self.client.put(update_url, valid_data, format='json', follow=True)
#         print(Article.objects.all())
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(Article.objects.count(), 1)
#         self.assertEqual(Article.objects.get().title, 'update_title')
#
#
# class CategoryApiTests(APITestCase):
#     def setUp(self):
#         self.client = APIClient(enforce_csrf_checks=True)
#         self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
#         self.client.force_authenticate(user=self.user)
#         self.url = reverse('view_categories')
#         self.data = {
#             'name': 'test_category',
#             'description': 'desc_category',
#         }
#         self.add_category = self.client.post(self.url, self.data, format='json', follow=True)
#
#     def test_valid_create_category(self):
#         valid_data = {
#             'name': 'valid_test_category',
#             'description': 'valid_desc_category',
#         }
#
#         response = self.client.post(self.url, valid_data, format='json', follow=True)
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(Category.objects.count(), 2)
#
#     def test_invalid_create_category(self):
#         invalid_data = {
#             'name': 'invalid_cat',
#             'description': '',  # empty
#         }
#
#         self.client.post(self.url, invalid_data, format='json', follow=True)
#         self.assertEqual(Category.objects.count(), 1)
#
#     def test_view_categories(self):
#         url = reverse('view_categories')
#         response = self.client.get(url, format='json', follow=True)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Category.objects.count(), 1)
#
#     def test_delete_category(self):
#         response_data = Category.objects.all()
#         print("Created: ", response_data)
#         self.assertEqual(len(response_data), 1)
#
#         factory = APIRequestFactory(enforce_csrf_checks=True)
#         view = SingleCategoryApiView.as_view()
#         request = factory.delete(reverse('change_categories', kwargs={'pk': 1}))
#         view(request, pk='1')
#         response_data = Category.objects.all()
#         print("Deleted: ", response_data)
#         self.assertEqual(len(response_data), 0)
#
#     def test_update_category(self):
#         update_url = reverse('change_categories', kwargs={'pk': 1})
#
#         valid_data = {
#             'name': 'update_cat',
#             'description': 'new_update_valid_desc_cat',
#         }
#         print(Category.objects.all())
#         response = self.client.put(update_url, valid_data, format='json', follow=True)
#         print(Category.objects.all())
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(Category.objects.count(), 1)
#         self.assertEqual(Category.objects.get().name, 'update_cat')
from comment.views import SingleCommentApiView


class CommentsApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.category = Category.objects.create(name='test_cat', description='test123')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('view_articles')
        self.data = {
            'title': 'test_title',
            'description': 'desc',
            'body': 'some_body',
            'category': self.category.id,
        }
        self.add_article = self.client.post(self.url, self.data, format='json', follow=True)

    def test_valid_create_comment(self):
        response = self.client.get(self.url, format='json', follow=True)
        response.render()
        valid_data = {
            'body': 'valid_test_comment',
            'article': json.loads(response.content)[0]['id'],
            'author': json.loads(str(self.user.id))
        }
        url = reverse('view_comments')
        response = self.client.post(url, valid_data, format='json', follow=True)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)

    def test_invalid_create_comment(self):
        response = self.client.get(self.url, format='json', follow=True)
        response.render()
        invalid_data = {
            'body': '',
            'article': json.loads(response.content)[0]['id'],
            'author': json.loads(str(self.user.id))
        }
        url = reverse('view_comments')
        self.client.post(url, invalid_data, format='json', follow=True)
        self.assertEqual(Comment.objects.count(), 0)

    def test_view_comments(self):
        response = self.client.get(self.url, format='json', follow=True)
        response.render()
        valid_data = {
            'body': 'valid_test_comment',
            'article': json.loads(response.content)[0]['id'],
            'author': json.loads(str(self.user.id))
        }
        url = reverse('view_comments')
        response = self.client.post(url, valid_data, format='json', follow=True)
        url = reverse('view_comments')
        response = self.client.get(url, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 1)

    def test_delete_category(self):
        response = self.client.get(self.url, format='json', follow=True)
        response.render()
        valid_data = {
            'body': 'valid_test_comment',
            'article': json.loads(response.content)[0]['id'],
            'author': json.loads(str(self.user.id))
        }
        url = reverse('view_comments')
        response = self.client.post(url, valid_data, format='json', follow=True)
        response_data = Comment.objects.all()
        print("Created: ", response_data)
        self.assertEqual(len(response_data), 1)

        factory = APIRequestFactory(enforce_csrf_checks=True)
        view = SingleCommentApiView.as_view()
        request = factory.delete(reverse('change_comments', kwargs={'pk': 1}))
        view(request, pk='1')
        response_data = Comment.objects.all()
        print("Deleted: ", response_data)
        self.assertEqual(len(response_data), 0)

    def test_update_category(self):
        update_url = reverse('change_comments', kwargs={'pk': 1})

        article_response = self.client.get(self.url, format='json', follow=True)
        article_response.render()
        valid_data = {
            'body': 'valid_test_comment',
            'article': json.loads(article_response.content)[0]['id'],
            'author': json.loads(str(self.user.id))
        }
        url = reverse('view_comments')
        response = self.client.post(url, valid_data, format='json', follow=True)
        print(Comment.objects.all())
        update_data = {
            'body': 'update_valid_test_comment',
            'article': json.loads(article_response.content)[0]['id'],
            'author': json.loads(str(self.user.id))
        }
        response = self.client.put(update_url, update_data, format='json', follow=True)
        print(Comment.objects.all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().body, 'update_valid_test_comment')
