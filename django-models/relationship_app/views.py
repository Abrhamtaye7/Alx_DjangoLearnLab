from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView

from .models import Book, Library


def list_books(request):
    books = Book.objects.select_related("author").all()
    return render(request, "relationship_app/list_books.html", {"books": books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


# --- Task 2: Authentication ---

class UserLoginView(LoginView):
    template_name = "relationship_app/login.html"


class UserLogoutView(LogoutView):
    template_name = "relationship_app/logout.html"


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # logs in right after registration
            return redirect("list_books")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


# --- Task 3: Role-based access control ---

def _role_is(role_name: str):
    def predicate(user):
        return (
            user.is_authenticated
            and hasattr(user, "profile")
            and user.profile.role == role_name
        )
    return predicate


@user_passes_test(_role_is("Admin"))
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(_role_is("Librarian"))
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(_role_is("Member"))
def member_view(request):
    return render(request, "relationship_app/member_view.html")


# --- Task 4: Custom permissions on Book CRUD ---

@permission_required("relationship_app.can_add_book", raise_exception=True)
def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        author_id = request.POST.get("author_id", "").strip()
        if title and author_id:
            from .models import Author
            author = get_object_or_404(Author, pk=author_id)
            Book.objects.create(title=title, author=author)
            return redirect("list_books")
    return render(request, "relationship_app/book_form.html", {"action": "Add"})


@permission_required("relationship_app.can_change_book", raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if title:
            book.title = title
            book.save()
            return redirect("list_books")
    return render(request, "relationship_app/book_form.html", {"action": "Edit", "book": book})


@permission_required("relationship_app.can_delete_book", raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("list_books")
    return render(request, "relationship_app/book_confirm_delete.html", {"book": book})
