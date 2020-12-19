from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from vote.models import VoteModel


class Tag(models.Model):
    tag = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.tag}'


class Article(VoteModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    tags = models.ManyToManyField(to=Tag, related_name='articles')

    def __str__(self):
        return f'"{self.title}" by {self.user.username}'


class Comment(VoteModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return f'"{self.body[:20]}..." on {self.article.title} by {self.user.username}'
