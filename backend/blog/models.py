from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from blog.managers import OrderedQuerySet, ArticleQuerySet


class Tag(models.Model):
    tag = models.SlugField(unique=True)
    objects = OrderedQuerySet.as_manager()

    def __str__(self):
        return f'{self.tag}'


class Vote(models.Model):
    VALUES = (
        ('UP', 1),
        ('DOWN', -1),
    )
    value = models.SmallIntegerField(choices=VALUES)
    user = models.ForeignKey(User, related_name='voter', on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.value}'


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    tags = models.ManyToManyField(to=Tag, related_name='articles')
    rating = models.SmallIntegerField(default=0)
    votes = GenericRelation(Vote)
    objects = ArticleQuerySet.as_manager()

    def __str__(self):
        return f'"{self.title}" by {self.user.username}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    rating = models.SmallIntegerField(default=0)
    votes = GenericRelation(Vote)
    objects = OrderedQuerySet.as_manager()

    def __str__(self):
        return f'"{self.body[:20]}..." on {self.article.title} by {self.user.username}'
