from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Book, Author
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book, Author


class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create a test user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a test author
        self.author = Author.objects.create(name="J.K. Rowling")

        # Create a test book
        self.book = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            author=self.author,
            publication_year=1997
        )

    def test_book_list(self):
        # Test for the list of books
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # One book exists
        self.assertEqual(response.data[0]['title'], "Harry Potter and the Philosopher's Stone")

    def test_book_detail(self):
        # Test for retrieving a single book
        url = reverse('book-detail', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Harry Potter and the Philosopher's Stone")

    def test_create_book(self):
        # Test for creating a book
        url = reverse('book-list')
        data = {
            "title": "Harry Potter and the Chamber of Secrets",
            "author": self.author.pk,
            "publication_year": 1998
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        # Test for updating a book
        url = reverse('book-detail', kwargs={'pk': self.book.pk})
        data = {
            "title": "Harry Potter and the Sorcerer's Stone",  # Updating the title
            "author": self.author.pk,
            "publication_year": 1997
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Harry Potter and the Sorcerer's Stone")

    def test_delete_book(self):
        # Test for deleting a book
        url = reverse('book-detail', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_search_book(self):
        # Test search functionality
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Harry Potter'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_book_by_year(self):
        # Test filtering by publication year
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 1997})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books_by_title(self):
        # Test ordering by title
        book2 = Book.objects.create(
            title="A Game of Thrones",
            author=self.author,
            publication_year=1996
        )
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "A Game of Thrones")


class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Create a test author
        self.author = Author.objects.create(name="J.K. Rowling")

        # Create a test book
        self.book = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            author=self.author,
            publication_year=1997
        )


def test_create_book(self):
    # Test for creating a book
    url = reverse('book-list')
    data = {
        "title": "Harry Potter and the Chamber of Secrets",
        "author": self.author.pk,
        "publication_year": 1998
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Book.objects.count(), 2)

