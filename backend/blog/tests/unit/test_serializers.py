from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from blog.serializers import UserSerializer, TagSerializer, ArticleSerializer, CommentSerializer
from blog.models import Tag, Article, Comment
from unittest.mock import MagicMock


class UserSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(username='test_username', email='test_email@example.com', password=make_password('test_password'))
        cls.test_user_serializer = UserSerializer(cls.test_user, context={'request': MagicMock()})

    def test_contains_expected_fields(self):
        data = self.test_user_serializer.data

        self.assertEqual(set(data.keys()), {'url', 'username', 'email'})

        print()

    def test_username_field_content(self):
        data = self.test_user_serializer.data

        self.assertEqual(data['username'], 'test_username')

    def test_update_email_field(self):
        self.test_user_serializer.update(self.test_user, {'email': 'test_email@mail.ru'})
        self.test_user.refresh_from_db()

        self.assertEqual(self.test_user.email, 'test_email@mail.ru')


class TagSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_tag = Tag.objects.create(tag='test_tag')
        cls.test_tag_serializer = TagSerializer(cls.test_tag, context={'request': MagicMock()})

    def test_contains_expected_fields(self):
        data = self.test_tag_serializer.data

        self.assertEqual(set(data.keys()), {'url', 'tag'})

    def test_tag_field_content(self):
        data = self.test_tag_serializer.data

        self.assertEqual(data['tag'], 'test_tag')

    def test_update_tag_field(self):
        self.test_tag_serializer.update(self.test_tag, {'tag': 'test_tag_02'})
        self.test_tag.refresh_from_db()

        self.assertEqual(self.test_tag.tag, 'test_tag_02')


class ArticleSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user_01 = User.objects.create(username='test_username_01', password=make_password('test_password_01'))
        cls.test_article_01 = Article.objects.create(title='test_title_01', body='test_body_01', user=cls.test_user_01)
        cls.test_article_01.votes.down(cls.test_user_01.pk)
        cls.test_article_01.refresh_from_db()
        cls.test_article_serializer = ArticleSerializer(cls.test_article_01, context={'request': RequestFactory().get('/')})

    def test_contains_expected_fields(self):
        data = self.test_article_serializer.data

        self.assertEqual(set(data.keys()), {'url', 'user', 'title', 'body', 'pub_date', 'tags', 'vote_score'})

    def test_title_field_content(self):
        data = self.test_article_serializer.data

        self.assertEqual(data['title'], 'test_title_01')

    def test_update_body_field(self):
        self.test_article_serializer.update(self.test_article_01, {'body': 'test_body_02'})
        self.test_article_01.refresh_from_db()

        self.assertEqual(self.test_article_01.body, 'test_body_02')


class CommentSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user_01 = User.objects.create(username='test_username_01', password=make_password('test_password_01'))
        cls.test_article_01 = Article.objects.create(title='test_title_01', body='test_body_01', user=cls.test_user_01)
        cls.test_comment_01 = Comment.objects.create(body='test_body_01', user_id=cls.test_user_01.pk, article_id=cls.test_article_01.pk)
        cls.test_comment_01.votes.up(cls.test_user_01.pk)
        cls.test_comment_01.refresh_from_db()
        cls.test_comment_serializer = CommentSerializer(cls.test_comment_01, context={'request': RequestFactory().get('/')})

    def test_contains_expected_fields(self):
        data = self.test_comment_serializer.data

        self.assertEqual(set(data.keys()), {'url', 'user', 'article', 'body', 'pub_date', 'vote_score'})

    def test_body_field_content(self):
        data = self.test_comment_serializer.data

        self.assertEqual(data['body'], 'test_body_01')

    def test_update_body_field(self):
        self.test_comment_serializer.update(self.test_comment_01, {'body': 'test_body_02'})
        self.test_comment_01.refresh_from_db()

        self.assertEqual(self.test_comment_01.body, 'test_body_02')
