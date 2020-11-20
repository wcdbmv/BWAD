from django.urls import path, include

from rest_framework import routers
from blog.views import UserViewSet, TagViewSet, VoteViewSet, ArticleViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('votes', VoteViewSet)
router.register('articles', ArticleViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
