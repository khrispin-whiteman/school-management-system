import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
import re
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from library.forms import IssueBookForm, BookAddForm, LibrarianAddForm, BookForm
from library.models import Book, Reviews, Borrower, Genre
from school.decorators import librarian_required, lecturer_required, student_required
from school.models import Student, User


@login_required
def librarian_list(request):
    """ Show list of all registered staff """
    librarian = User.objects.filter(is_student=False, is_lecturer=False, is_parent=False, is_superuser=False)
    user_type = "Librarian"
    context = {
        "librarian": librarian,
        "user_type": user_type,
    }
    return render(request, 'library/librarians_list.html', context)


@login_required
def BookCreate(request):
    if not request.user.is_librarian:
        return redirect('BookListView')
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('BookListView')
    return render(request, 'library/add_book.html', locals())


@method_decorator([login_required, lecturer_required], name='dispatch')
class LibrarianAddView(CreateView):
    model = User
    form_class = LibrarianAddForm
    template_name = 'library/add_librarian.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'librarian'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('librarian_list')


# @method_decorator([login_required, librarian_required], name='dispatch')
# class AddBookView(CreateView):
#     model = Book
#     form_class = BookAddForm
#     template_name = 'library/add_book.html'
#
#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'book'
#         return super().get_context_data(**kwargs)
#
#     def form_valid(self, form):
#         form.save()
#         return redirect('BookListView')




@login_required
def BookListView(request):
    book_list = Book.objects.all()
    # MODELNAME.objects.all() is used to get all objects i.e. tuples from database
    return render(request, 'library/books.html',
                  {
                      'book_list': book_list,
                  })


@login_required
def BookDetailView(request, pk):
    book = get_object_or_404(Book, id=pk)
    reviews=Reviews.objects.filter(book=book).exclude(review="none")
    try:
        stu = Student.objects.get(roll_no=request.user)
        rr=Reviews.objects.get(review="none")
    except:
        pass
    return render(request, 'library/book_detail.html', locals())


@login_required
def BookDelete(request, pk):
    if not request.user.is_superuser:
        return redirect('BookListView')
    obj = get_object_or_404(Book, pk=pk)
    obj.delete()
    return redirect('BookListView')


@method_decorator([login_required, librarian_required], name='dispatch')
class IssueBookView(CreateView):
    model = Borrower
    form_class = IssueBookForm
    template_name = 'library/issue_book.html'

    def form_valid(self, form):
        form.save()
        return redirect('book_borrowers')


@login_required
def book_borrowers(request):
    borrowers_list = Borrower.objects.all()
    # MODELNAME.objects.all() is used to get all objects i.e. tuples from database
    return render(request, 'library/borrowers.html',
                  {
                      'borrowers_list': borrowers_list,
                  })


@login_required
def student_request_issue(request, pk):
    obj = Book.objects.get(id=pk)
    stu=Student.objects.get(roll_no=request.user)
    s = get_object_or_404(Student, roll_no=str(request.user))
    if s.total_books_due < 10:
        message = "book has been issued, You can collect book from library"
        a = Borrower()
        a.student = s
        a.book = obj
        a.issue_date = datetime.datetime.now()
        obj.available_copies = obj.available_copies - 1
        obj.save()
        stu.total_books_due=stu.total_books_due+1
        stu.save()
        a.save()
    else:
        message = "you have exceeded limit."
    return render(request, 'catalog/result.html', locals())


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def search_book(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['title', 'summary','author'])

        book_list= Book.objects.filter(entry_query)

    return render(request,'library/books.html',locals() )