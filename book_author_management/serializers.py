from rest_framework import serializers
from .models import Book, BorrowingHistory,Author,UserBookReview

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name','date_of_birth','country']


class BookSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = ['id', 'title', 'ISBN', 'authors', 'publication_date', 'copies_available','status','average_rating']
    def get_average_rating(self, obj):
        return obj.average_rating()

class BorrowingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowingHistory
        fields = ['id', 'book', 'user', 'borrow_date', 'return_date','status']


class UserBookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookReview
        fields = ['user', 'book', 'review', 'rating']

        