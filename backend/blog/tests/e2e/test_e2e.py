from http import HTTPStatus
from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Tag, Article, Comment
import os


class RingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.passed = 0

    def __get(self, model_class):
        return model_class.objects.all().first()

    def get_user(self):
        return self.__get(User)

    def get_tag(self):
        return self.__get(Tag)

    def get_article(self):
        return self.__get(Article)

    def get_comment(self):
        return self.__get(Comment)

    def test_live(self):
        self.n = int(os.getenv('TEST_REPEATS', 100))
        self.passed = 0

        for i in range(self.n):
            self.__test_live()

    def tearDown(self):
        print(f'{self.passed}/{self.n}')

    def __test_live(self):
        #
        # Create user
        #
        response = self.client.post(
            '/api/v1/users/',
            data={
                'username': 'username',
                'email': 'user@example.com',
                'password': 'password',
            })

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(self.get_user().username, 'username')

        #
        # Create tag
        #
        self.client.force_login(self.get_user())
        user = response.json()['url']
        response = self.client.post(
            '/api/v1/tags/',
            data={
                'tag': 'tag',
            })

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(self.get_tag().tag, 'tag')

        #
        # Create article
        #
        tag = response.json()['url']
        response = self.client.post(
            '/api/v1/articles/',
            data={
                'user': user,
                'title': 'title',
                'body': 'body',
                'tags': [
                    tag,
                ],
            })

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(self.get_article().title, 'title')

        #
        # Create comment
        #
        article = response.json()['url']
        article_id = article[article[:-1].rfind('/')+1:-1]
        response = self.client.post(
            '/api/v1/comments/',
            data={
                'user': user,
                'article': article,
                'body': 'body',
            })

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(self.get_comment().body, 'body')

        #
        # Downvote article
        #
        comment = response.json()['url']
        comment_id = comment[comment[:-1].rfind('/')+1:-1]
        response = self.client.post(
            f'/api/v1/articles/{article_id}/vote/',
            data={
                'action': 'down'
            })

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(self.get_article().vote_score, -1)

        #
        # Try to downvote article again
        #
        response = self.client.post(
            f'/api/v1/articles/{article_id}/vote/',
            data={
                'action': 'down'
            })

        self.assertEqual(response.status_code, HTTPStatus.CONFLICT)
        self.assertEqual(self.get_article().vote_score, -1)

        #
        # Upvote comment
        #
        response = self.client.post(
            f'/api/v1/comments/{comment_id}/vote/',
            data={
                'action': 'up'
            })

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(self.get_comment().vote_score, 1)

        #
        # Try to upvote comment again
        #
        response = self.client.post(
            f'/api/v1/comments/{comment_id}/vote/',
            data={
                'action': 'up'
            })

        self.assertEqual(response.status_code, HTTPStatus.CONFLICT)
        self.assertEqual(self.get_comment().vote_score, 1)

        #
        # Delete vote from comment
        #
        response = self.client.delete(f'/api/v1/comments/{comment_id}/vote/')

        self.assertEqual(response.status_code, HTTPStatus.OK)

        #
        # Delete vote from article
        #
        response = self.client.delete(f'/api/v1/articles/{article_id}/vote/')

        self.assertEqual(response.status_code, HTTPStatus.OK)

        #
        # Delete comment
        #
        response = self.client.delete(f'/api/v1/comments/{comment_id}/')

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

        #
        # Delete article
        #
        response = self.client.delete(f'/api/v1/articles/{article_id}/')

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

        #
        # Total
        #
        self.passed += 1

        #
        # Cleanup
        #
        Tag.objects.all().delete()
        User.objects.all().delete()
