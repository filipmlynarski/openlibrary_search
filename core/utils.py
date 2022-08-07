from collections import Counter
from functools import lru_cache

import requests
from rest_framework import status

from core.models import AuthorSearches, BookSearches

URL_FORMAT = (
    'http://openlibrary.org/search.json'
    '?author={author}&fields=author_key,author_name,key,title'
)


class InvalidQueryException(Exception):
    pass


@lru_cache
def fetch_openlibrary(author: str) -> list[dict]:
    request = requests.get(URL_FORMAT.format(author=author))
    if request.status_code == status.HTTP_200_OK:
        return request.json()['docs']
    raise InvalidQueryException()


def create_analytics(docs: list[dict]) -> None:
    author_counts = Counter()
    book_counts = Counter()
    for doc in docs:
        author_counts.update(zip(doc['author_key'], doc['author_name']))
        book_counts[(doc['key'], doc['title'])] += 1

    existing_authors = AuthorSearches.objects.filter(
        author_key__in={author_key for author_key, _ in author_counts},
    )
    existing_books = BookSearches.objects.filter(
        key__in={key for key, _ in book_counts},
    )
    author_objs = {author.author_key: author for author in existing_authors}
    book_objs = {book.key: book for book in existing_books}

    _create_author_searches(
        author_counts=author_counts,
        author_objs=author_objs,
    )
    _create_book_searches(
        book_counts=book_counts,
        book_objs=book_objs,
    )


def _create_author_searches(
        author_counts: dict[tuple[str, str], int],
        author_objs: dict[str, AuthorSearches],
) -> None:
    authors_to_update = []
    authors_to_create = []
    for (author_key, author_name), count in author_counts.items():
        if author_obj := author_objs.get(author_key):
            author_obj.count += count
            authors_to_update.append(author_obj)
        else:
            authors_to_create.append(
                AuthorSearches(
                    author_key=author_key,
                    author_name=author_name,
                    count=count,
                ),
            )
    AuthorSearches.objects.bulk_update(authors_to_update, ['count'])
    AuthorSearches.objects.bulk_create(authors_to_create)


def _create_book_searches(
        book_counts: dict[tuple[str, str], int],
        book_objs: dict[str, BookSearches],
) -> None:
    books_to_update = []
    books_to_create = []
    for (key, title), count in book_counts.items():
        if book_obj := book_objs.get(key):
            book_obj.count += count
            books_to_update.append(book_obj)
        else:
            books_to_create.append(
                BookSearches(
                    key=key,
                    title=title,
                    count=count,
                ),
            )
    BookSearches.objects.bulk_update(books_to_update, ['count'])
    BookSearches.objects.bulk_create(books_to_create)
