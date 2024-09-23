from django.db import models
from authentication.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

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
    

    def average_rating(self):
        average = UserBookReview.objects.filter(book=self).aggregate(Avg('rating'))
        return average['rating__avg'] if average['rating__avg'] is not None else 0.0
    

    

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
    


class BorrowPending(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('pending', 'pending'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    def __str__(self):
        return self.user
    

class UserBookReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name='books')
    review = models.TextField()
    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])

    def __str__(self):
        return f"{self.user.username}'s review of {self.book.title} (Rating: {self.rating})"
    

    


    

