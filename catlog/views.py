from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    """View function for home page of site."""

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genre = Genre.objects.all().count()
    num_book_contains_c = Book.objects.filter(title__icontains='c').count()
    
    # Using session
    num_visit = request.session.get('num_visit', 0)
    num_visit += 1
    request.session['num_visit'] = num_visit
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre' : num_genre,
        'num_book_contains_c' : num_book_contains_c,
        'num_visit' : num_visit,
    } 
    
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'catlog/book_list.html'
    paginate_by = 2
    
    def get_queryset(self):
        return Book.objects.all().order_by('title')[:5]
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        # for data in context:
            
        return context
    

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catlog/book_detail.html'
    
    
class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'catlog/author_list'
    
    
class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catlog/author_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catlog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )