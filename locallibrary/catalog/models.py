
from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances
from datetime import date

# Create your models here.
class Genre(models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""

    name = models.CharField(
        max_length=200, 
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books

    summary = models.CharField(
        max_length=1000,
        help_text="Enter a brief description of the book")

    isbn = models.CharField(
        max_length=13, 
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    # ManyToManyField used because a genre can contain many books and a Book can cover many genres.

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Avaliable'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1, 
        choices=LOAN_STATUS, 
        blank=True, default='m', 
        help_text='Book availability')
    
    class META:
        ordering = ['due_back']

    def __str__ (self):
        """String for representing the Model object."""
        return '{0} ({1})'.format(self.id, self.book.title)    

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0} {1}'.format(self.last_name, self.first_name)

class Language(models.Model):
    "Enter the book's natural language (e.g. English, French, Japanese etc.)"
    name = models.CharField(
        max_length=50,
        help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)"
        )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name