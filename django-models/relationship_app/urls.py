from django.urls import path
from .views import (
    LibraryDetailView,
    UserLoginView,
    UserLogoutView,
    add_book,
    admin_view,
    delete_book,
    edit_book,
    librarian_view,
    list_books,
    member_view,
    register,
)

urlpatterns = [
    # Task 1
    path("books/", list_books, name="list_books"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    # Task 2
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),

    # Task 3
    path("role/admin/", admin_view, name="admin_view"),
    path("role/librarian/", librarian_view, name="librarian_view"),
    path("role/member/", member_view, name="member_view"),

    # Task 4
    path("books/add/", add_book, name="add_book"),
    path("books/<int:pk>/edit/", edit_book, name="edit_book"),
    path("books/<int:pk>/delete/", delete_book, name="delete_book"),
]
