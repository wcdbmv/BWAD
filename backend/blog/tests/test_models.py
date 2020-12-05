from django.test import TestCase
# from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from blog.models import Tag, Article, Comment
from blog.tests.user_builder import UserBuilder


def make_password_stub(s):
    return s


class TagTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_tag_01 = Tag.objects.create(tag='test_tag_01')
        cls.test_tag_02 = Tag.objects.create(tag='test_taq_02')

    def test_get_tag_by_tag(self):
        test_tag_01 = Tag.objects.get(tag='test_tag_01')
        test_tag_02 = Tag.objects.get(tag='test_taq_02')

        self.assertEqual(test_tag_01.tag, 'test_tag_01')
        self.assertEqual(test_tag_02.tag, 'test_taq_02')

    def test_get_not_existing_tag(self):
        throw_exception = False

        try:
            Tag.objects.get(tag='test_tag_03')
        except Tag.DoesNotExist:
            throw_exception = True

        self.assertTrue(throw_exception)

    def test_fix_typo_in_tag(self):
        Tag.objects.filter(tag='test_taq_02').update(tag='test_tag_02')

        self.test_tag_02.refresh_from_db()
        self.assertEqual(self.test_tag_02.tag, 'test_tag_02')


class ArticleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user_01 = UserBuilder('test_username_01').with_password(make_password_stub('test_password_01')).build()
        cls.test_user_02 = UserBuilder('test_username_02').with_password(make_password_stub('test_password_02')).build()

        cls.test_article_01 = Article.objects.create(title='test_title_01', body='test_body_01', user=cls.test_user_01)
        cls.test_article_02 = Article.objects.create(title='test_title_02', body='test_body_02', user=cls.test_user_02)
        cls.test_article_01.votes.up(cls.test_user_02.pk)
        cls.test_article_02.votes.down(cls.test_user_01.pk)
        cls.test_article_01.refresh_from_db()
        cls.test_article_02.refresh_from_db()

    def test_to_string(self):
        expected_string_test_article_01 = '"test_title_01" by test_username_01'
        expected_string_test_article_02 = '"test_title_02" by test_username_02'

        str_test_article_01 = str(self.test_article_01)
        str_test_article_02 = str(self.test_article_02)

        self.assertEqual(str_test_article_01, expected_string_test_article_01)
        self.assertEqual(str_test_article_02, expected_string_test_article_02)

    def test_update_vote_score(self):
        expected_test_article_01_vote_score = 2
        expected_test_article_02_vote_score = -2

        self.test_article_01.votes.up(self.test_user_01.pk)
        self.test_article_02.votes.down(self.test_user_02.pk)

        self.test_article_01.refresh_from_db()
        self.test_article_02.refresh_from_db()
        self.assertEqual(self.test_article_01.vote_score, expected_test_article_01_vote_score)
        self.assertEqual(self.test_article_02.vote_score, expected_test_article_02_vote_score)

    def test_delete_vote_score(self):
        expected_test_article_01_vote_score = 0
        expected_test_article_02_vote_score = 0

        self.test_article_01.votes.delete(self.test_user_01.pk)
        self.test_article_01.votes.delete(self.test_user_02.pk)
        self.test_article_02.votes.delete(self.test_user_01.pk)
        self.test_article_02.votes.delete(self.test_user_02.pk)

        self.test_article_01.refresh_from_db()
        self.test_article_02.refresh_from_db()
        self.assertEqual(self.test_article_01.vote_score, expected_test_article_01_vote_score)
        self.assertEqual(self.test_article_02.vote_score, expected_test_article_02_vote_score)


class CommentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user_01 = User.objects.create(username='test_username_01', password=make_password_stub('test_password_01'))
        cls.test_user_02 = User.objects.create(username='test_username_02', password=make_password_stub('test_password_02'))

        cls.test_article_01 = Article.objects.create(title='test_title_01', body='test_body_01', user=cls.test_user_01)

        cls.test_comment_01 = Comment.objects.create(body='test_body_01', user_id=cls.test_user_01.pk, article_id=cls.test_article_01.pk)
        cls.test_comment_02 = Comment.objects.create(body='test_body_02', user_id=cls.test_user_02.pk, article_id=cls.test_article_01.pk)
        cls.test_comment_01.votes.up(cls.test_user_02.pk)
        cls.test_comment_02.votes.down(cls.test_user_01.pk)
        cls.test_comment_01.refresh_from_db()
        cls.test_comment_02.refresh_from_db()

    def test_to_string(self):
        expected_string_test_comment_01 = '"test_body_01..." on test_title_01 by test_username_01'
        expected_string_test_comment_02 = '"test_body_02..." on test_title_01 by test_username_02'

        str_test_comment_01 = str(self.test_comment_01)
        str_test_comment_02 = str(self.test_comment_02)

        self.assertEqual(str_test_comment_01, expected_string_test_comment_01)
        self.assertEqual(str_test_comment_02, expected_string_test_comment_02)

    def test_update_vote_score(self):
        expected_test_comment_01_vote_score = 2
        expected_test_comment_02_vote_score = -2

        self.test_comment_01.votes.up(self.test_user_01.pk)
        self.test_comment_02.votes.down(self.test_user_02.pk)

        self.test_comment_01.refresh_from_db()
        self.test_comment_02.refresh_from_db()
        self.assertEqual(self.test_comment_01.vote_score, expected_test_comment_01_vote_score)
        self.assertEqual(self.test_comment_02.vote_score, expected_test_comment_02_vote_score)

    def test_delete_vote_score(self):
        expected_test_comment_01_vote_score = 0
        expected_test_comment_02_vote_score = 0

        self.test_comment_01.votes.delete(self.test_user_01.pk)
        self.test_comment_01.votes.delete(self.test_user_02.pk)
        self.test_comment_02.votes.delete(self.test_user_01.pk)
        self.test_comment_02.votes.delete(self.test_user_02.pk)

        self.test_comment_01.refresh_from_db()
        self.test_comment_02.refresh_from_db()
        self.assertEqual(self.test_comment_01.vote_score, expected_test_comment_01_vote_score)
        self.assertEqual(self.test_comment_02.vote_score, expected_test_comment_02_vote_score)
