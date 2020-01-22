from django.contrib import admin

# Register your models here.
#library
from library.models import Genre, Language, Book, Borrower, Reviews


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_display_links = ('name', )
    list_per_page = 10
    search_fields = ('name', )

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_display_links = ('name', )
    list_per_page = 10
    search_fields = ('name', )


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'summary', 'isbn', 'language', 'total_copies', 'available_copies', 'pic')
    list_display_links = ('title', 'author', 'summary', 'isbn', 'language', 'total_copies', 'available_copies', 'pic')
    list_per_page = 10
    search_fields = ('title', 'author', 'summary', 'isbn', 'language__name', 'total_copies', 'available_copies', )


class BorrowerAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'num_books_borrowed', 'issue_date', 'return_date', 'returned')
    list_display_links = ('student', 'book', 'num_books_borrowed', 'issue_date', 'return_date', 'returned')
    list_per_page = 10
    search_fields = ('student__user', 'book__title', 'num_books_borrowed', 'issue_date', 'return_date', 'returned')


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('review', 'book', 'student', 'rating')
    list_display_links = ('review', 'book', 'student', 'rating')
    list_per_page = 10
    search_fields = ('review', 'book', 'student', 'rating')





admin.site.register(Genre, GenreAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Borrower, BorrowerAdmin)
admin.site.register(Reviews, ReviewsAdmin)