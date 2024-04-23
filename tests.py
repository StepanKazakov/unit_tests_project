import pytest


# Test class for BooksCollector
class TestBooksCollector:
    @pytest.mark.parametrize('name', [
        'I',                                         # Single character, boundary value
        'Проверка максимальной длины названия рус',  # Maximum valid length, boundary value
        'Sherlock Holmes',                           # Normal valid name
        '1984',                                      # Numeric characters in string format
        "'@#$%^&*()'"                                # Special characters in string format
    ])
    def test_add_new_book_check_boundary_values_positive(self, collector, my_books, name):
        collector.add_new_book(name)
        assert len(my_books) == 1
        assert name in my_books
        assert my_books[name] == ''

    def test_add_new_book_check_boundary_values_negative(self, collector, my_books):
        collector.add_new_book('')                   # Empty name
        collector.add_new_book('i'*41)               # More than 40 characters
        assert len(my_books) == 0

    def test_set_book_genre_add_book_and_genre_successful(self, collector, my_books):
        collector.add_new_book('Dune')
        collector.set_book_genre('Dune', 'Фантастика')
        assert my_books['Dune'] == 'Фантастика'

    def test_set_book_genre_set_genre_to_nonexistent_book_result_none(self, collector):
        collector.set_book_genre('Nonexistent', 'Мультфильмы')
        assert collector.get_book_genre('Nonexistent') is None

    def test_set_book_genre_set_nonexistent_genre_to_book_result_not_set(self, collector, my_books):
        collector.add_new_book('Sherlock Holmes')
        collector.set_book_genre('Sherlock Holmes', 'Детектив')
        assert my_books['Sherlock Holmes'] == ''

    def test_set_book_genre_change_genre_return_last_value(self, collector, my_books):
        collector.add_new_book('1984')
        collector.set_book_genre('1984', 'Фантастика')
        assert my_books['1984'] == 'Фантастика'
        collector.set_book_genre('1984', 'Комедии')
        assert my_books['1984'] == 'Комедии'
        assert my_books['1984'] != 'Фантастика'

    def test_get_books_with_specific_genre_fiction_only(self, collector, my_books):
        assert len(my_books) == 0
        collector.add_new_book('Star Wars')
        collector.add_new_book('Sherlock Holmes')
        collector.set_book_genre('Star Wars', 'Фантастика')
        collector.set_book_genre('Sherlock Holmes', 'Детективы')
        fiction = collector.get_books_with_specific_genre('Фантастика')
        assert len(my_books) == 2
        assert len(fiction) == 1
        assert 'Star Wars' in fiction

    def test_get_books_for_children_exclude_age_restricted_genre(self, collector, my_books):
        assert len(my_books) == 0
        collector.add_new_book('Metro 2033')
        collector.set_book_genre('Metro 2033', 'Ужасы')
        collector.add_new_book('Alice')
        collector.set_book_genre('Alice', 'Мультфильмы')
        children_books = collector.get_books_for_children()
        assert len(my_books) == 2
        assert len(children_books) == 1
        assert 'Metro 2033' not in children_books

    def test_add_book_in_favorites_check_and_remove(self, collector, my_favorite):
        assert my_favorite == []
        collector.add_new_book('Metro 2035')
        collector.add_book_in_favorites('Metro 2035')
        assert 'Metro 2035' in my_favorite
        collector.delete_book_from_favorites('Metro 2035')
        assert 'Metro 2035' not in my_favorite

    def test_add_book_in_favorites_double_add_list_of_favorites_return_one(self, collector, my_favorite):
        assert my_favorite == []
        collector.add_new_book('Lord of the ring')
        collector.add_book_in_favorites('Lord of the ring')
        collector.set_book_genre('Lord of the ring', 'Фантастика')
        collector.add_book_in_favorites('Lord of the ring')
        assert len(my_favorite) == 1
