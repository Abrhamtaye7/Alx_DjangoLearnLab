"""
Run with:
python manage.py shell < relationship_app/query_samples.py
(or paste into shell)
"""

from relationship_app.models import Author, Book, Library, Librarian


# 1) Query all books by a specific author.
author_name = "Chinua Achebe"
author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)
print("Books by author:", author_name, list(books_by_author))

# 2) List all books in a library.
library_name = "Central Library"
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()
print("Books in library:", library_name, list(books_in_library))

# 3) Retrieve the librarian for a library.
librarian = Librarian.objects.get(library=library)
print("Librarian for library:", library_name, librarian)
