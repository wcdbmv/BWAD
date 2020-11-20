from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from votes.managers import VotableManager
from blog.managers import OrderedQuerySet, ArticleQuerySet


class Tag(models.Model):
    tag = models.SlugField(unique=True)
    objects = OrderedQuerySet.as_manager()

    def __str__(self):
        return f'{self.tag}'


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    tags = models.ManyToManyField(to=Tag, related_name='articles')
    rating = models.SmallIntegerField(default=0)
    votes = VotableManager()
    objects = ArticleQuerySet.as_manager()

    def __str__(self):
        return f'"{self.title}" by {self.user.username}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    rating = models.SmallIntegerField(default=0)
    votes = VotableManager()
    objects = OrderedQuerySet.as_manager()

    def __str__(self):
        return f'"{self.body[:20]}..." on {self.article.title} by {self.user.username}'
