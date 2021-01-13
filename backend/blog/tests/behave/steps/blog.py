import requests
from behave import *

from django.contrib.auth.models import User
from blog.models import Article

use_step_matcher("re")

USERNAME = 'test-behave-user'
EMAIL = 'test-behave@example.com'
PASSWORD = 'test-behave-password'
ARTICLE_TITLE = 'test-behave-title'
ARTICLE_BODY = 'test-behave-body'
COMMENT_BODY = 'Good article!'


@step('An url')
def step_impl(context):
    context.url = context.test_case.live_server_url
    print(context.url)


@step('I create profile')
def step_impl(context):
    context.response_create_user = requests.post(f'{context.url}/users/', data={
        'username': USERNAME,
        'email': EMAIL,
        'password': PASSWORD,
    })
    context.response_create_user_json = context.response_create_user.json()


@step('log in')
def step_impl(context):
    context.response_log_in = requests.post(f'{context.url}/api-auth/login/', data={
        'username': USERNAME,
        'password': PASSWORD,
    })
    context.response_log_in_json = context.response_log_in.json()


@step('create article')
def step_impl(context):
    context.response_create_article = requests.post(f'{context.url}/api/v1/articles/', data={
        'user': f'{context.url}/api/v1/users/{User.objects.get(username=USERNAME).pk}/',
        'title': ARTICLE_TITLE,
        'body': ARTICLE_BODY,
    })
    context.response_create_article_json = context.response_create_article.json()


@step('create comment "Good article!"')
def step_impl(context):
    context.response_create_comment = requests.post(f'{context.url}/api/v1/comments/', data={
        'user': f'{context.url}/api/v1/users/{User.objects.get(username=USERNAME).pk}/',
        'article': f'{context.url}/api/v1/articles/{Article.objects.get(title=ARTICLE_TITLE)}/',
        'body': COMMENT_BODY,
    })
    context.response_create_comment_json = context.response_create_comment.json()


@then('I should see "Good article!" in page')
def step_impl(context):
    context.response_get_comments = requests.get(f'{context.url}/api/v1/comments/').text
    assert COMMENT_BODY in context.response_get_comments
