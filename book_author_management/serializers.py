from rest_framework import serializers
from .models import Book, BorrowingHistory,Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name','date_of_birth','country']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'ISBN', 'authors', 'publication_date', 'copies_available','status']

class BorrowingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowingHistory
        fields = ['id', 'book', 'user', 'borrow_date', 'return_date','status']

        