from django.db import models
from authentication.models import CustomUser

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    



class Book(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
    ]
    title = models.CharField(max_length=255)
    ISBN = models.CharField(max_length=13, unique=True)  # ISBN-13 format
    authors = models.ManyToManyField(Author)
    publication_date = models.DateField()
    copies_available = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.title
    

    

class BorrowingHistory(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrowed')

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title} on {self.borrow_date}"
