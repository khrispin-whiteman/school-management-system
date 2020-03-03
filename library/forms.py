from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from library.models import Book, Borrower, Genre, Language
from school.models import User, Student


#add book by librarian
class BookAddForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Title",
        max_length=100,
        required=False)

    author = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Author",
        max_length=100,
        required=False)

    summary = forms.TextInput()

    isbn = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="ISBN",
        max_length=16,
        required=False)

    genre = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Language',
    )

    total_copies = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Number Of Books Available",
        max_length=16)

    pic = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Upload picture",
        required=False)

    class Meta:
        model = Book
        fields = ['title', 'author',
                  'summary', 'isbn', 'genre', 'language', 'total_copies', 'pic']

    def save(self, **kwargs):
        book = super().save(commit=False)
        book.pic = self.cleaned_data.get('pic')
        book.save()
        return book


class IssueBookForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Student',
    )

    book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Book',
    )

    num_books_borrowed = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label="*No of Books Borrowed",
    )

    return_date = forms.DateTimeField(
        label="Return Date",
        widget=forms.SelectDateWidget
    )

    returned = forms.BooleanField(
        label="*Book Returned",
        required=False
    )


    class Meta:
        model = Borrower
        fields = ['student', 'book', 'num_books_borrowed', 'return_date', 'returned']


class LibrarianAddForm(UserCreationForm):
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Address",
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Mobile No.",
    )

    firstname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Firstname",
    )

    lastname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Lastname",
    )

    email = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Email",
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_librarian = True
        user.first_name = self.cleaned_data.get('firstname')
        user.last_name = self.cleaned_data.get('lastname')
        user.phone = self.cleaned_data.get('phone')
        user.address = self.cleaned_data.get('address')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name']