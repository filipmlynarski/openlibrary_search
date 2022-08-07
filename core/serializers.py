from rest_framework import serializers

from core.models import AuthorSearches, BookSearches


class AuthorSearchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorSearches
        fields = ('author_key', 'author_name', 'count')


class BookSearchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSearches
        fields = ('key', 'title', 'count')
