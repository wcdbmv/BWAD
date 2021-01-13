import os
import django
from django.test.runner import DiscoverRunner
from django.test.testcases import LiveServerTestCase
from behave import fixture, use_fixture
import os


@fixture
def django_test_runner(context):
    django.setup()
    context.test_runner = DiscoverRunner()
    context.test_runner.setup_test_environment()
    context.old_db_config = context.test_runner.setup_databases()
    yield
    context.test_runner.teardown_databases(context.old_db_config)
    context.test_runner.teardown_test_environment()


@fixture
def django_test_case(context):
    context.test_case = LiveServerTestCase
    context.test_case.setUpClass()
    yield
    context.test_case.tearDownClass()
    del context.test_case


os.environ["DJANGO_SETTINGS_MODULE"] = "test_project.settings"


def before_all(context):
    use_fixture(django_test_runner, context)


def before_scenario(context, scenario):
    use_fixture(django_test_case, context)
