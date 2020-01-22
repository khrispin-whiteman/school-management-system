from django.urls import path
from library import views
from library.views import IssueBookView

urlpatterns = [
    path('library/librarians', views.librarian_list, name='librarian_list'),
    path('library/new/', views.LibrarianAddView.as_view(), name="add_new_librarian"),
    path('library/books', views.BookListView, name='BookListView'),
    #path('library/books/new/', views.AddBookView.as_view(), name='AddBookView'),
    path('library/books/new/', views.BookCreate, name='AddBookView'),
    path('library/book/<int:pk>', views.BookDetailView, name='book-detail'),
    path('library/search_b/', views.search_book, name="search_b"),
    path('library/book/<int:pk>/request_issue/', views.student_request_issue, name='request_issue'),
    path('library/books/issue/', IssueBookView.as_view(), name='IssueBookView'),
    path('library/books/borrowers/', views.book_borrowers, name='book_borrowers'),
]