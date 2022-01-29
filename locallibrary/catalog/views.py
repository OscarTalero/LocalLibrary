from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre

# Create your views here.

def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Avaliable Books (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()
    num_genres=Genre.objects.all().count()
    num_books_word=Book.objects.filter(title__contains='mundo').count()
    
    # Render the template HTML index.html whit the data in context variable
    return render (
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,
                 'num_instances_available':num_instances_available,
                 'num_authors':num_authors, 'num_genres':num_genres,
                 'num_books_word':num_books_word}
        )

class BookListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Book
    paginate_by = 10
    
class BookDetailView(generic.DetailView):
    model = Book
    
class AuthorListView(generic.ListView):
    """Generic class-based view for a list of authors."""
    model = Author
    
class AuthorDetailView(generic.DetailView):
    model = Author
    