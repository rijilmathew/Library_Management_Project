from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Book, BorrowingHistory
from .serializers import BookSerializer, BorrowingHistorySerializer
from django.utils import timezone

# Create your views here.


class IsStaffUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_staff_user()

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffUser]

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffUser]

    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        if BorrowingHistory.objects.filter(book=book, return_date__isnull=True).exists():
            raise PermissionDenied("Cannot delete a book with outstanding borrowing records.")
        return super().delete(request, *args, **kwargs)

class BorrowingHistoryListView(generics.ListAPIView):
    queryset = BorrowingHistory.objects.all()
    serializer_class = BorrowingHistorySerializer
    permission_classes = [IsStaffUser]