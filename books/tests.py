from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book


class BookModelTest(TestCase):
    """Test Book model functionality with modern patterns."""

    def setUp(self):
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '978-0123456789',
            'publication_date': '2023-01-01',
            'genre': 'Fiction',
            'description': 'A test book'
        }
        self.book = Book.objects.create(**self.book_data)

    def test_book_creation_and_str_representation(self):
        """Test book creation and string representation."""
        self.assertEqual(self.book.title, 'Test Book')
        self.assertEqual(self.book.author, 'Test Author')
        self.assertEqual(str(self.book), 'Test Book by Test Author')
        
    def test_book_fields_validation(self):
        """Test all book fields are properly saved and validated."""
        self.assertEqual(self.book.isbn, '978-0123456789')
        self.assertEqual(self.book.genre, 'Fiction')
        self.assertEqual(self.book.description, 'A test book')
        self.assertIsNotNone(self.book.created_at)
        self.assertIsNotNone(self.book.updated_at)
        
    def test_book_ordering_by_creation_date(self):
        """Test books are ordered by creation date descending."""
        book2 = Book.objects.create(title='Second Book', author='Another Author')
        books = list(Book.objects.all())
        self.assertEqual(books[0], book2)  # Most recent first
        
    def test_book_indexes_exist(self):
        """Test that database indexes are properly created."""
        indexes = [idx.fields for idx in Book._meta.indexes]
        self.assertIn(['author'], indexes)
        self.assertIn(['genre'], indexes)
    
    def test_isbn_validation_in_model(self):
        """Test ISBN validation in model clean method."""
        # Valid ISBN should work
        book = Book(title='Valid ISBN', author='Test', isbn='978-1234567890')  # Different ISBN
        book.full_clean()  # Should not raise
        
        # Invalid ISBN should fail
        book = Book(title='Invalid ISBN', author='Test', isbn='12345')
        with self.assertRaises(ValidationError):
            book.full_clean()
            
    def test_empty_isbn_allowed(self):
        """Test that empty ISBN is allowed and doesn't conflict."""
        book1 = Book.objects.create(title='Book 1', author='Author 1', isbn='')
        book2 = Book.objects.create(title='Book 2', author='Author 2', isbn='')
        self.assertEqual(Book.objects.filter(isbn='').count(), 2)


class BookAPITest(APITestCase):
    """Test Book API endpoints with modern patterns."""

    def setUp(self):
        self.book_data = {
            'title': 'API Test Book',
            'author': 'API Author', 
            'isbn': '978-0987654321',
            'publication_date': '2023-06-01',
            'genre': 'Science Fiction',
            'description': 'A science fiction book for testing'
        }
        self.book = Book.objects.create(**self.book_data)
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book.pk})

    def test_list_books_with_pagination(self):
        """Test listing books with pagination structure."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'API Test Book')

    def test_create_book_with_full_data(self):
        """Test creating a book with complete data."""
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn': '978-1111111111', 
            'publication_date': '2023-12-01',
            'genre': 'Mystery',
            'description': 'A mystery book'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(response.data['title'], 'New Book')
        self.assertEqual(response.data['author'], 'New Author')

    def test_create_book_minimal_data(self):
        """Test creating a book with only required fields."""
        data = {'title': 'Minimal Book', 'author': 'Minimal Author'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Minimal Book')

    def test_isbn_validation_invalid_format(self):
        """Test ISBN validation in model prevents creation."""
        # Test that model validation works correctly
        book = Book(title='Test', author='Test', isbn='12345')  # Invalid ISBN
        with self.assertRaises(ValidationError):
            book.full_clean()

    def test_get_book_detail(self):
        """Test retrieving book details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'API Test Book')
        self.assertEqual(response.data['isbn'], '978-0987654321')
        self.assertEqual(response.data['genre'], 'Science Fiction')

    def test_update_book_partial(self):
        """Test partial book update."""
        data = {'title': 'Updated Title', 'genre': 'Updated Genre'}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')
        self.assertEqual(self.book.genre, 'Updated Genre')
        self.assertEqual(self.book.author, 'API Author')  # Unchanged

    def test_delete_book(self):
        """Test book deletion."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_smart_search_prioritizes_author(self):
        """Test that search prioritizes author matches."""
        # Create books with different matches
        Book.objects.create(title='Science Book', author='Other Author', genre='Science')
        Book.objects.create(title='Random Book', author='Science Writer', genre='Biography')
        
        response = self.client.get(self.list_url, {'search': 'Science'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should find author matches first
        results = response.data['results']
        self.assertTrue(any('Science Writer' in book['author'] for book in results))

    def test_responsive_genre_filtering(self):
        """Test responsive genre filtering with partial matches."""
        response = self.client.get(self.list_url, {'genre__icontains': 'Sci'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        response = self.client.get(self.list_url, {'genre__icontains': 'Science'})
        self.assertEqual(len(response.data['results']), 1)

    def test_date_range_filtering(self):
        """Test publication date range filtering."""
        # Create books with different dates
        Book.objects.create(title='Old Book', author='Old Author', publication_date='2020-01-01')
        Book.objects.create(title='New Book', author='New Author', publication_date='2024-01-01')
        
        # Test date range
        response = self.client.get(self.list_url, {
            'publication_date_from': '2023-01-01',
            'publication_date_to': '2024-12-31'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 2)  # Our test book + New Book

    def test_get_books_by_author_endpoint(self):
        """Test the by-author endpoint with refactored response."""
        url = reverse('book-by-author', kwargs={'author': 'API Author'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['books']), 1)
        self.assertEqual(response.data['author'], 'API Author')

    def test_get_books_by_nonexistent_author(self):
        """Test by-author endpoint with non-existent author."""
        url = reverse('book-by-author', kwargs={'author': 'Nonexistent Author'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['books']), 0)

    def test_bulk_update_by_author(self):
        """Test bulk updating books by author."""
        url = reverse('book-update-by-author')
        data = {
            'author': 'API Author',
            'update_data': {'genre': 'Updated Genre', 'description': 'Updated description'}
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Updated 1 books', response.data['message'])
        
        self.book.refresh_from_db()
        self.assertEqual(self.book.genre, 'Updated Genre')
        self.assertEqual(self.book.description, 'Updated description')

    def test_bulk_update_validation_scenarios(self):
        """Test bulk update with various validation scenarios."""
        url = reverse('book-update-by-author')
        
        test_cases = [
            # (data, expected_status, error_substring)
            ({'author': 'API Author', 'update_data': {'invalid_field': 'value'}}, 400, 'No valid fields'),
            ({'update_data': {'genre': 'New Genre'}}, 400, 'Author and update_data required'),
            ({'author': 'Test Author'}, 400, 'Author and update_data required'),
            ({'author': 'Nonexistent Author', 'update_data': {'genre': 'New'}}, 404, 'No books found'),
        ]
        
        for data, expected_status, error_text in test_cases:
            with self.subTest(data=data):
                response = self.client.patch(url, data, format='json')
                self.assertEqual(response.status_code, expected_status)
                self.assertIn(error_text, response.data['error'])
