from django.db import models


class OrderedQuerySet(models.QuerySet):
    def newest(self):
        return self.order_by('-pub_date')

    def oldest(self):
        return self.order_by('pub_date')

    def most_rated(self):
        return self.order_by('-rating')

    def least_rated(self):
        return self.order_by('rating')


class ArticleQuerySet(OrderedQuerySet):
    def tags(self, tag):
        return self.filter(tags__tag=tag)

    def users(self, user):
        return self.filter(user=user)

    def comments(self, article_id):
        return self.get(id=article_id).comment_set
