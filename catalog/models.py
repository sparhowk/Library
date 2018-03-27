from django.db import models
from django.urls import reverse
from django.utils import timezone
import uuid


class Genre(models.Model):
    """
        Model prezentujący kategorie i rodzaj ksiązek (np. Fantastyka )
    """
    
    name = models.CharField(max_length=250,
                            help_text="Wprowadź kategorię książki")
    
    def __str__(self):
        """
            String for representic the Model object (in Admin site etc.)
        """
        
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Podaj język książki")
    
    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    website = models.URLField()
    
    def __str__(self):
        return self.name



class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    data_of_birth = models.DateField(null=True,
                                     blank=True)
    data_of_dead = models.DateField('Died',
                                    null=True,
                                    blank=True)    
        
    class Meta:
        ordering = ["last_name", "first_name"]
        
    
    def __str__(self):
        return '{} {}'.format(self.last_name, self.first_name)


class Book(models.Model):
    title = models.CharField(max_length=300)
    title_orginal = models.CharField(max_length=300,
                                     null=True,
                                     blank=True)
    author = models.ManyToManyField(Author,
                                    #on_delete=models.SET_NULL,
                                    )
    slug = models.SlugField(max_length=250,
                            unique_for_date='create')
    summary = models.TextField(max_length=1000,
                               help_text="Wprowadź krótki opis książki")
    isbn = models.CharField('ISBN', 
                            max_length=13,
                            help_text='Wprowadź 13 znakowy <a href="https://www.isbn-international.org/content/what-isbn"> numer ISBN</a>',
                            null=True)
    genre = models.ManyToManyField(Genre,
                                   help_text="Podaj kategorię dla tej ksiązki")
    language = models.ForeignKey('Language',
                                 on_delete=models.SET_NULL,
                                 null=True)
    create = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now=True)
    
    
    def display_genre(self):
        """
            Creates a string for the Genre. This is required ti display genre in Admin
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
        display_genre.short_description = 'Genre'
    
    
    def display_author(self):
        return ', '.join([(author.last_name, author.first_name) for author in self.author.all()[:2]])
        display_author.short_description = 'Author'
    
    
    def __str__(self):
        return "{} {}".format(self.title, self.author.last_name, self.author.first_name)
    
    
    def get_absolute_url(self):
        """
            Returns the url to access a detail record for this book.
        """
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """
        Model representing a specific copy of a book
    """
    STATUS = (
        ('p', 'Published'),
        ('u', 'Unpublised'),
        ('d', 'Deleted')
    )
    
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          help_text="Unikalny identyfikator tej książki w całej bibliotece")
    book = models.ForeignKey('Book',
                             on_delete=models.SET_NULL,
                             null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True,
                                blank=True)
    publish = models.DateField(default=timezone.now)
    status = models.CharField(max_length=1,
                              choices=STATUS,
                              blank=True,
                              default='u',
                              help_text='Book Status')
    
    
    class Meta:
        ordering = ["publish"]
    
    
    def __str__(self):
        return '{} ({})'.format(self.id, self.book.title)


        