from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.test import APITestCase

from article.models import Article, Category

# initialize the APIClient app
from article.serializers import ArticleSerializer




# class GetAllArticlesTest(TestCase):
#     """ Test module for GET all puppies API """
#     def setUp(self):
#         user = User.objects.create_user(username='test', password='test123')
#         user.save()
#         author = get_object_or_404(User, id=1)
#         Article.objects.create(
#             title='Casper', description=3, body='Bull Dog', author=author)
#         Article.objects.create(
#             title='Casper1', description=3, body='Bull Dog', author=author)
#         Article.objects.create(
#             title='Casper2', description=3, body='Bull Dog', author=author)
#
#     def test_get_all_puppies(self):
#         # get API response
#         response = client.get(reverse('blog_index'))
#         # get data from db
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


class ArticleTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        # self.user = User.objects.create_user(username='test_user', password='test123')
        self.category = Category.objects.create(name='test_cat', description='test123')
        self.client.login(username='john', password='johnpassword')
        print(Category.objects.get(id=1))
        print(User.objects.get(id=1))
        # category = get_object_or_404(Category, id=1)
        url = reverse('blog_add')
        data = {
            'title': 'DabApps',
            'description': 'desc',
            'body': 'yea',
            'author': self.user.id,
            'category': self.category.id,
        }
        response = self.client.post(url, data, format='json', follow=True)
        print(Article.objects.get())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().title, 'DabApps')
