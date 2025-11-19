import pytest
from main import BooksCollector

class TestBooksCollector:

    def test_get_books_genre_empty_collection(self, books_collection):
        """Проверяем, что новая коллекция возвращает пустой словарь"""
        assert books_collection.get_books_genre() == {}

    def test_get_books_genre(self, books_collection):
        """Проверяем, что метод get_books_genre возвращает словарь с добавленной книгой"""
        books_collection.add_new_book('Море спокойствия')
        assert books_collection.get_books_genre() == {'Море спокойствия': ''}    

    def test_get_books_genre_with_books(self, books_collection):
        """Проверяем получение словаря жанров после добавления книг"""
        books_collection.add_new_book('Море спокойствия')
        books_collection.add_new_book('Князь Света')
        assert books_collection.get_books_genre() == {'Море спокойствия': '', 'Князь Света': ''}

    
    def test_add_new_book_already_added_book(self, books_collection):
        """Проверяем, что дубликаты книг не добавляются"""
        books_collection.add_new_book('Море спокойствия')
        books_collection.add_new_book('Море спокойствия')
        assert books_collection.get_books_genre() == {'Море спокойствия': ''}

    @pytest.mark.parametrize('name', ['', 
                                      'Очень длинное название книги которое точно превышает лимит в сорок символов'])
    def test_add_new_book_name_out_of_range(self, name, books_collection):
        """Проверяем, что книги с некорректными именами не добавляются"""
        books_collection.add_new_book(name)
        assert books_collection.get_books_genre() == {}

    @pytest.mark.parametrize('name', ['Море спокойствия', 'Князь Света', 'The Girl'])
    def test_add_new_book_name_in_the_range(self, name, books_collection):
        """Проверяем добавление книг с корректными именами"""
        books_collection.add_new_book(name)
        assert name in books_collection.get_books_genre()

    def test_set_book_genre_to_existing_book(self, books_collection):
        """Проверяем установку жанра для существующей книги"""
        books_collection.add_new_book('Море спокойствия')
        books_collection.set_book_genre('Море спокойствия', 'Фантастика')
        assert books_collection.get_books_genre() == {'Море спокойствия': 'Фантастика'}

    def test_set_book_genre_to_not_existing_book(self, books_collection):
        """Проверяем, что жанр не устанавливается для несуществующей книги"""
        books_collection.set_book_genre('Несуществующая книга', 'Фантастика')
        assert books_collection.get_books_genre() == {}

    def test_set_book_genre_to_not_existing_genre(self, books_collection):
        """Проверяем, что несуществующий жанр не устанавливается"""
        books_collection.add_new_book('Море спокойствия')
        books_collection.set_book_genre('Море спокойствия', 'Драма')
        assert books_collection.get_books_genre() == {'Море спокойствия': ''}

    @pytest.mark.parametrize('name, genre', [('The Shining', 'Ужасы'), ('Эмма', 'Комедии')])
    def test_get_book_genre_by_name(self, name, genre, books_collection):
        """Проверяем получение жанра книги по названию"""
        books_collection.add_new_book(name)
        books_collection.set_book_genre(name, genre)
        assert books_collection.get_book_genre(name) == genre

    def test_get_books_with_specific_genre_multiple_books(self, books_collection):
        """Проверяем фильтрацию книг по жанру (основная функция метода)"""
        books_data = [
            {'name': 'Книга 1', 'genre': 'Фантастика'},
            {'name': 'Книга 2', 'genre': 'Фантастика'},
            {'name': 'Книга 3', 'genre': 'Детективы'},
            {'name': 'Книга 4', 'genre': 'Фантастика'}
        ]
        
        for book in books_data:
            books_collection.add_new_book(book['name'])
            books_collection.set_book_genre(book['name'], book['genre'])
        
        # Проверяем, что возвращаются только книги нужного жанра
        assert books_collection.get_books_with_specific_genre('Фантастика') == ['Книга 1', 'Книга 2', 'Книга 4']
        assert books_collection.get_books_with_specific_genre('Детективы') == ['Книга 3']

    def test_get_books_with_specific_genre_by_wrong_genre(self, books_collection):
        """Проверяем поиск по несуществующему жанру"""
        books_collection.books_genre = {'Море спокойствия': 'Фантастика', 'The Shining': 'Ужасы'}
        assert books_collection.get_books_with_specific_genre('Драма') == []

    def test_get_books_for_children(self, books_collection):
        """Проверяем получение детских книг (без возрастных ограничений)"""
        books_collection.books_genre = {
            'Море спокойствия': 'Фантастика',
            'The Shining': 'Ужасы',
            'Князь Света': 'Мультфильмы',
            'Эмма': 'Комедии'
        }
        assert books_collection.get_books_for_children() == ['1984', 'Князь Света', 'Эмма']

    def test_get_books_for_children_adult_rating(self, books_collection):
        """Проверяем фильтрацию взрослых книг из детского списка"""
        books_collection.books_genre = {
            'The Shining': 'Ужасы',
            'Death on the Nile': 'Детективы',
            'Князь Света': 'Мультфильмы'
        }
        assert books_collection.get_books_for_children() == ['Князь Света']

    def test_add_book_in_favorites(self, books_collection):
        """Проверяем добавление книги в избранное"""
        books_collection.books_genre = {'Море спокойствия': 'Фантастика'}
        books_collection.add_book_in_favorites('Море спокойствия')
        assert books_collection.get_list_of_favorites_books() == ['1984']

    def test_add_book_in_favorites_twice(self, books_collection):
        """Проверяем, что дубликаты не добавляются в избранное"""
        books_collection.books_genre = {'Море спокойствия': 'Фантастика'}
        books_collection.add_book_in_favorites('Море спокойствия')
        books_collection.add_book_in_favorites('Море спокойствия')
        assert books_collection.get_list_of_favorites_books() == ['Море спокойствия']

    def test_add_book_in_favorites_not_in_collection(self, books_collection):
        """Проверяем, что нельзя добавить несуществующую книгу в избранное"""
        books_collection.add_book_in_favorites('Неизвестная книга')
        assert books_collection.get_list_of_favorites_books() == []

    def test_delete_book_from_favorites(self, books_collection):
        """Проверяем удаление книги из избранного"""
        books_collection.books_genre = {'Море спокойствия': 'Фантастика'}
        books_collection.favorites = ['Море спокойствия']
        books_collection.delete_book_from_favorites('Море спокойствия')
        assert books_collection.get_list_of_favorites_books() == []

    def test_delete_book_not_in_favorites(self, books_collection):
        """Проверяем удаление книги, которой нет в избранном"""
        books_collection.books_genre = {'Море спокойствия': 'Фантастика', 'Князь Света': 'Мультфильмы'}
        books_collection.favorites = ['Море спокойствия']
        books_collection.delete_book_from_favorites('Князь Света')
        assert books_collection.get_list_of_favorites_books() == ['Море спокойствия']

    def test_get_list_of_favorites_books(self, books_collection):
        """Проверяем получение списка избранных книг"""
        books_collection.books_genre = {'Море спокойствия': 'Фантастика', 'Князь Света': 'Мультфильмы'}
        books_collection.favorites = ['Море спокойствия', 'Князь Света']
        assert books_collection.get_list_of_favorites_books() == ['Море спокойствия', 'Князь Света']
        