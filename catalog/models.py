from django.db import models
from django.urls import reverse



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


class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.ManyToManyField('Autor',
                                    #on_delete=models.SET_NULL,
                                    null=True)
    summary = models.TextField(max_length=1000,
                               help_text="Wprowadź krótki opis książki")
    isbn = models.CharField('ISBN', 
                            max_length=13,
                            help_text='Wprowadź 13 znakowy <a href="https://www.isbn-international.org/content/what-isbn"> numer ISBN</a>',
                            null=True)
    genre = models.ManyToManyField(Genre,
                                   help_text="Podaj kategorię dla tej ksiązki")

    
    def __str__(self):
        return "{} {}".format(self.author, self.title)
    
    
    def get_absolute_url(self):
        """
            Returns the url to access a detail record for this book.
        """
        return reverse('book-detail', args=[str(self.id)])

class Author(models.Model):
    pass
        
        
        