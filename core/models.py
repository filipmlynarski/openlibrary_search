from django.db import models


class AuthorSearches(models.Model):
    author_key = models.CharField(primary_key=True, max_length=128)
    author_name = models.CharField(max_length=128)
    count = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'author searches'


class BookSearches(models.Model):
    key = models.CharField(primary_key=True, max_length=128)
    title = models.CharField(max_length=128)
    count = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'book searches'
