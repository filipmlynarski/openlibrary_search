import csv

from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import AuthorSearches, BookSearches
from core.serializers import AuthorSearchesSerializer, BookSearchesSerializer
from core.utils import (
    create_analytics,
    fetch_openlibrary,
    InvalidQueryException,
)


class SearchLibraryView(APIView):
    @staticmethod
    def get(request, author: str):
        try:
            docs = fetch_openlibrary(author)
        except InvalidQueryException:
            return Response(
                {'error': 'invalid query'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            create_analytics(docs)
            return Response(docs, status=status.HTTP_200_OK)


class SearchLibraryCSVView(APIView):
    @staticmethod
    def get(request, author: str):
        try:
            docs = fetch_openlibrary(author)
        except InvalidQueryException:
            return Response(
                {'error': 'invalid query'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        create_analytics(docs)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="search.csv"'
        writer = csv.DictWriter(
            response,
            fieldnames=['author_key', 'author_name', 'key', 'title'],
        )
        writer.writeheader()
        writer.writerows(docs)

        return response


class AuthorSearchesDetailView(RetrieveAPIView):
    queryset = AuthorSearches.objects.all()
    serializer_class = AuthorSearchesSerializer
    lookup_field = 'author_key'


class BookSearchesDetailView(RetrieveAPIView):
    queryset = BookSearches.objects.all()
    serializer_class = BookSearchesSerializer
    lookup_field = 'key'
