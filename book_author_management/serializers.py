from rest_framework import serializers
from .models import Book, BorrowingHistory,Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'ISBN', 'authors', 'publication_date', 'copies']

class BorrowingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowingHistory
        fields = ['id', 'book', 'user', 'borrowed_at', 'returned_at']