import pytest
from main import BooksCollector

@pytest.fixture
def books_collection():
    books_collection = BooksCollector()
    return books_collection