from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from blog.views import UserViewSet, TagViewSet, ArticleViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('articles', ArticleViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('openapi', get_schema_view(
        title="Blog",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
    path('', TemplateView.as_view(template_name='blog/swagger-ui.html'), name='swagger-ui'),
    path('', include(router.urls)),
]
