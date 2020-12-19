from http import HTTPStatus
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from vote.models import Vote
from blog.models import Article


class RegistrationTest(TestCase):
    def test_registration_success(self):
        user_data = {
            'username': 'username',
            'email': 'user@example.com',
            'password': 'password',
        }

        response = self.client.post('/api/v1/users/', data=user_data)
        try:
            created_user = User.objects.get(username=user_data['username'])
            is_user_created = True
        except User.DoesNotExist:
            created_user = {'email': None}
            is_user_created = False

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue(is_user_created)
        self.assertEqual(created_user.email, user_data['email'])

    def test_registration_already_exists(self):
        User.objects.create(
            username='username',
            email='user@example.com',
            password=make_password('password'),
        )

        user_data = {
            'username': 'username',
            'first_name': 'first_name',
            'email': 'user@example.com',
            'password': 'password',
        }

        response = self.client.post('/api/v1/users/', data=user_data)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertRaises(User.DoesNotExist, User.objects.get, first_name='first_name')


@patch('vote.signals.post_voted.send', autospec=True)
class VoteArticlesTest(TestCase):
    def test_like_success(self, mock_post_voted_send):
        user = User.objects.create(
            username='username',
            email='user@example.com',
            password=make_password('password'),
        )

        article = Article.objects.create(
            user_id=user.pk,
            title='title',
            body='body',
        )

        self.client.force_login(user)
        response = self.client.post(f'/api/v1/articles/{article.pk}/vote/')
        article.refresh_from_db()
        try:
            Vote.objects.get(pk=1)
            is_vote_created = True
        except Vote.DoesNotExist:
            is_vote_created = False

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(is_vote_created)
        self.assertEqual(article.vote_score, 1)
        self.assertTrue(mock_post_voted_send.called)

    def test_like_already_exist(self, mock_post_voted_send):
        user = User.objects.create(
            username='username',
            email='user@example.com',
            password=make_password('password'),
        )

        article = Article.objects.create(
            user_id=user.pk,
            title='title',
            body='body',
        )

        article.votes.up(user.pk)
        vote = Vote.objects.get(pk=1)

        self.client.force_login(user)
        response = self.client.post(f'/api/v1/articles/{article.pk}/vote/')
        article.refresh_from_db()
        try:
            Vote.objects.get(pk=1)
            is_vote_still_exists = True
        except Vote.DoesNotExist:
            is_vote_still_exists = False

        self.assertEqual(response.status_code, HTTPStatus.CONFLICT)
        self.assertTrue(is_vote_still_exists)
        self.assertEqual(article.vote_score, 1)
        self.assertFalse(mock_post_voted_send.called)
