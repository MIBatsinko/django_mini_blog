from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.utils import json

from article.models import Article, Category
from comment.models import Comment


class ArticleWebTests(APITestCase):
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
            'category': self.category.name,
        }
        self.add_article = self.client.post(self.url, self.data, format='json', follow=True)

    def test_valid_create_article(self):
        data = {
            'title': 'new_valid_title',
            'description': 'new_valid_desc',
            'body': 'new_valid_body',
            'category': self.category.name,
        }
        self.add_new_valid_article = self.client.post(self.url, data, format='json', follow=True)
        self.assertEqual(self.add_new_valid_article.status_code, 200)
        articles = self.client.get(reverse('blog_index'), format='json', follow=True).context.get('blog')
        self.assertEqual(len(articles), 2)

    def test_invalid_create_article(self):
        data = {
            'title': 'invalid article',
            'description': '',  # empty
            'body': 'some body',
            'author': self.user.id,
            'category': self.category.name,
        }

        self.client.post(self.url, data, format='json', follow=True)
        self.assertEqual(Article.objects.count(), 1)

    def test_view_articles(self):
        url = reverse('blog_index')
        response = self.client.get(url, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.context['blog']
        self.assertEqual(len(data), 1)

    def test_rendering_responses(self):
        articles = self.client.get(reverse('blog_index'), format='json', follow=True).context.get('blog')

        url = reverse('blog_view', kwargs={'pk': articles[0].id})
        self.client.get(url, format='json', follow=True)
        data = {
            'id': articles[0].id,
            'title': articles[0].title,
        }
        self.assertEqual(data, {"id": articles[0].id, "title": articles[0].title})

    def test_delete_article(self):
        articles = self.client.get(reverse('blog_index'), format='json', follow=True).context.get('blog')
        print("Created: ", articles)
        self.assertEqual(len(articles), 1)

        url = reverse('blog_delete', kwargs={'pk': articles[0].id})
        self.client.delete(url, format='json', follow=True)
        articles = self.client.get(reverse('blog_index'), format='json', follow=True).context.get('blog')
        print("Deleted: ", articles)
        self.assertEqual(len(articles), 0)

    def test_update_article(self):
        articles = self.client.get(reverse('blog_index'), format='json', follow=True).context.get('blog')
        update_url = reverse('blog_edit', kwargs={'pk': articles[0].id})
        # GET the form
        response = self.client.get(update_url)
        print(response.context.keys())
        # retrieve form data as dict
        form = response.context['form']
        data = form.initial  # form is unbound but contains data
        print("Before update: ",
              Article.objects.get(id=articles[0].id).title,
              Article.objects.get(id=articles[0].id).description,
              Article.objects.get(id=articles[0].id).body)
        # manipulate some data
        data['title'] = 'updated_value'

        # POST to the form
        self.client.post(update_url, data)

        # retrieve again
        response = self.client.get(update_url)
        print("After update: ",
              Article.objects.get(id=articles[0].id).title,
              Article.objects.get(id=articles[0].id).description,
              Article.objects.get(id=articles[0].id).body)

        self.assertContains(response, 'updated_value')  # or
        self.assertEqual(response.context['form'].initial['title'], 'updated_value')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().title, 'updated_value')


class ArticleApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        # token = Token.objects.get(user__username='john')
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.category = Category.objects.create(name='test_cat', description='test123')
        self.client.force_authenticate(user=self.user)

        self.client.login(username='john', password='johnpassword')
        self.url = reverse('view_articles')
        self.data = {
            'title': 'test_title',
            'description': 'desc',
            'body': 'some_body',
            'category': self.category.id,
        }
        self.add_article = self.client.post(self.url, self.data, format='json', follow=True)
        self.add_article.render()

        self.articles_url = reverse('view_articles')

    def test_valid_create_article(self):
        valid_data = {
            'title': 'new_valid_title',
            'description': 'new_valid_desc',
            'body': 'new_valid_body',
            'category': self.category.id,
        }

        response = self.client.post(self.url, valid_data, format='json', follow=True)
        articles = json.loads(self.client.get(self.articles_url, format='json', follow=True).content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[1].get('author').get('username'), self.user.username)

    def test_invalid_create_article(self):
        invalid_data = {
            'title': 'invalid article',
            'description': '',  # empty
            'body': 'some body',
            'author': self.user.id,
            'category': self.category.id,
        }

        articles = json.loads(self.client.get(self.articles_url, format='json', follow=True).content)
        self.client.post(self.url, invalid_data, format='json', follow=True)
        self.assertEqual(len(articles), 1)

    def test_view_articles(self):
        url = reverse('view_articles')
        response = self.client.get(url, format='json', follow=True)
        articles = json.loads(self.client.get(self.articles_url, format='json', follow=True).content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(articles), 1)

    def test_check_response_data(self):
        response = self.client.get(reverse('change_articles', kwargs={'pk': 1}), format='json')
        response.render()
        data = {
            'id': json.loads(response.content)['id'],
            'title': json.loads(response.content)['title']
        }
        self.assertEqual(data, {'id': 1, 'title': 'test_title'})

    def test_delete_article(self):
        articles = json.loads(self.client.get(self.articles_url, format='json', follow=True).content)
        print("Created: ", articles, len(articles))
        self.assertEqual(len(articles), 1)

        self.client.delete(reverse('change_articles', kwargs={'pk': articles[0].get('id')}), format='json')

        response_data = json.loads(self.client.get(self.articles_url, format='json', follow=True).content)
        print("Deleted: ", response_data, len(response_data))
        self.assertEqual(len(response_data), 0)

    def test_update_article(self):
        articles = json.loads(self.client.get(self.articles_url, format='json', follow=True).content)
        update_url = reverse('change_articles', kwargs={'pk': articles[0].get('id')})

        valid_data = {
            'title': 'update_title',
            'description': 'new_update_valid_desc',
            'body': 'new_valupdate_id_body',
            'category': self.category.id,
        }

        articles = json.loads(self.client.get(self.articles_url, format='json', follow=True).content)
        print("Before:", articles)
        response = self.client.put(update_url, valid_data, format='json', follow=True)
        articles = json.loads(self.client.get(self.articles_url, format='json', follow=True).content)
        print("After: ", articles)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].get('title'), 'update_title')


class CategoryApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('view_categories')
        self.data = {
            'name': 'test_category',
            'description': 'desc_category',
        }
        self.client.login(username='john', password='johnpassword')
        self.add_category = self.client.post(self.url, self.data, format='json', follow=True)

    def test_valid_create_category(self):
        valid_data = {
            'name': 'valid_test_category',
            'description': 'valid_desc_category',
        }

        response = self.client.post(self.url, valid_data, format='json', follow=True)
        categories = json.loads(self.client.get(self.url, format='json', follow=True).content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(categories), 2)

    def test_invalid_create_category(self):
        invalid_data = {
            'name': 'invalid_cat',
            'description': '',  # empty
        }

        self.client.post(self.url, invalid_data, format='json', follow=True)
        categories = json.loads(self.client.get(self.url, format='json', follow=True).content)

        self.assertEqual(len(categories), 1)

    def test_view_categories(self):
        response = self.client.get(self.url, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_delete_category(self):
        categories = json.loads(self.client.get(self.url, format='json', follow=True).content)
        print("Created: ", categories)
        self.assertEqual(len(categories), 1)

        self.client.delete(reverse('change_categories', kwargs={'pk': categories[0].get('id')}), format='json')

        categories = json.loads(self.client.get(self.url, format='json', follow=True).content)

        print("Deleted: ", categories)
        self.assertEqual(len(categories), 0)

    def test_update_category(self):
        categories = json.loads(self.client.get(self.url, format='json', follow=True).content)
        update_url = reverse('change_categories', kwargs={'pk': categories[0].get('id')})

        valid_data = {
            'name': 'update_cat',
            'description': 'new_update_valid_desc_cat',
        }
        print(categories)
        response = self.client.put(update_url, valid_data, format='json', follow=True)
        categories = json.loads(self.client.get(self.url, format='json', follow=True).content)
        print(categories)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, 'update_cat')


class CommentsApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.category = Category.objects.create(name='test_cat', description='test123')
        self.client.force_authenticate(user=self.user)
        self.client.login(username='john', password='johnpassword')
        self.url = reverse('view_articles')
        self.data = {
            'title': 'test_title',
            'description': 'desc',
            'body': 'some_body',
            'category': self.category.id,
        }
        self.add_article = self.client.post(self.url, self.data, format='json', follow=True)
        self.add_article.render()

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

    def test_delete_comment(self):
        response = self.client.get(self.url, format='json', follow=True)
        response.render()
        valid_data = {
            'body': 'valid_test_comment',
            'article': json.loads(response.content)[0]['id'],
            'author': json.loads(str(self.user.id))
        }
        url = reverse('view_comments')
        self.client.post(url, valid_data, format='json', follow=True)
        comments = json.loads(self.client.get(url, format='json', follow=True).content)
        print("Created: ", comments)
        self.assertEqual(len(comments), 1)

        self.client.delete(reverse('change_comments', kwargs={'pk': comments[0].get('id')}), format='json')
        comments = json.loads(self.client.get(url, format='json', follow=True).content)
        print("Deleted: ", comments)
        self.assertEqual(len(comments), 0)

    def test_update_comment(self):
        article_response = self.client.get(self.url, format='json', follow=True)
        article_response.render()
        valid_data = {
            'body': 'valid_test_comment',
            'article': json.loads(article_response.content)[0]['id'],
            'author': json.loads(str(self.user.id))
        }
        url = reverse('view_comments')
        self.client.post(url, valid_data, format='json', follow=True)
        print(Comment.objects.all())
        update_data = {
            'body': 'update_valid_test_comment',
            'article': json.loads(article_response.content)[0]['id'],
            'author': json.loads(str(self.user.id))
        }
        comments = json.loads(self.client.get(url, format='json', follow=True).content)
        update_url = reverse('change_comments', kwargs={'pk': comments[0].get('id')})
        response = self.client.put(update_url, update_data, format='json', follow=True)
        comments = json.loads(self.client.get(url, format='json', follow=True).content)
        print(comments)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].get('body'), 'update_valid_test_comment')


class UserApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.user1 = User.objects.create_user('john1', 'lennon1@thebeatles.com', 'johnpassword')
        self.user2 = User.objects.create_user('john2', 'lennon2@thebeatles.com', 'johnpassword')
        self.user3 = User.objects.create_user('john3', 'lennon3@thebeatles.com', 'johnpassword')
        self.client.login(username='john2', password='johnpassword')
        self.users_url = reverse('view_users')

    def test_view_users(self):
        response = self.client.get(self.users_url)
        response.render()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 3)

    def test_view_user(self):
        users = json.loads(self.client.get(self.users_url, format='json', follow=True).content)
        user_url = reverse('view_user', kwargs={'pk': users[1].get('id')})
        response = self.client.get(user_url, follow=True)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content).get('username'), users[1].get('username'))

    # def test_update_user(self):
    #     update_data = {'username': 'jfgfffg', 'first_name': 'hjhjh', 'last_name': 'kkhkjk', 'email': 'lennon1@thebeatles.com', 'avatar': '/media/avatar.png'}
    #     update_url = reverse('edit_user')
    #     response = self.client.put(update_url, update_data, format='json', follow=True)
    #     users = json.loads(self.client.get(self.users_url, format='json', follow=True).content)
    #     print(users)
    #     # self.assertEqual(response.status_code, 200)
    #     response.render()
    #     print(json.loads(response.content))
    #     self.assertEqual(len(users), 3)
    #     self.assertEqual(users[0].get('username'), update_data.get('username'))
