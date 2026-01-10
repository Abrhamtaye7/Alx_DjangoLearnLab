
**delete.md**
```md
```python
from bookshelf.models import Book
book = Book.objects.get(id=1)
book.delete()
# Expected output: (1, {'bookshelf.Book': 1})

Book.objects.all()
# Expected output: <QuerySet []>
