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


@step('My account')
def step_impl(context):
    context.user = User.objects.create_user(USERNAME, email=EMAIL, password=PASSWORD)

    br = context.browser
    br.get(context.base_url + '/api-auth/login/')
    br.find_element_by_name('username').send_keys(USERNAME)
    br.find_element_by_name('password').send_keys(PASSWORD)
    br.find_element_by_name('submit').click()


@step('exists article')
def step_impl(context):
    context.article = Article.objects.create(
        user=context.user,
        title=ARTICLE_TITLE,
        body=ARTICLE_BODY,
    )


from time import sleep


@step('I create comment "Good article!"')
def step_impl(context):
    br = context.browser
    br.get(context.base_url + '/api/v1/')
    br.find_element_by_css_selector('#operations-api-createComment').click()
    br.find_element_by_css_selector('#operations-api-createComment .try-out__btn').click()
    textarea = br.find_element_by_css_selector('#operations-api-createComment .body-param__text')
    textarea.clear()
    textarea.send_keys(
        f'{{'
        f'"user": "{context.base_url}/api/v1/users/{context.user.pk}/", '
        f'"article": "{context.base_url}/api/v1/articles/{context.article.pk}/", '
        f'"body": "{COMMENT_BODY}"'
        f'}}'
    )
    br.find_element_by_css_selector('#operations-api-createComment .execute').click()
    br.find_element_by_css_selector('#operations-api-createComment .execute').click()


@then('I should see "Good article!" in page')
def step_impl(context):
    br = context.browser
    br.get(f'{context.base_url}/api/v1/comments/')
    sleep(5)
    assert COMMENT_BODY in br.page_source
