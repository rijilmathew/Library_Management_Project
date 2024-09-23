from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Book, BorrowingHistory,Author,BorrowPending,UserBookReview
from .serializers import BookSerializer, BorrowingHistorySerializer,AuthorSerializer,UserBookReviewSerializer
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission



# Create your views here.


class IsStaffUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_staff_user()
    
class IsBookReturnUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view)

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffUser]

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        if BorrowingHistory.objects.filter(book=book, return_date__isnull=True).exists():
            raise PermissionDenied("Cannot delete a book with outstanding borrowing records.")
        return super().delete(request, *args, **kwargs)

class BorrowingHistoryListView(generics.ListAPIView):
    queryset = BorrowingHistory.objects.all()
    serializer_class = BorrowingHistorySerializer
    permission_classes = [IsStaffUser]



class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsStaffUser]

class AuthorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsStaffUser]

    def delete(self, request, *args, **kwargs):
        author = self.get_object()
        if author.books.exists():
            return Response({'error': 'Cannot delete author with associated books.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().delete(request, *args, **kwargs)
    

#Public Book Search and Borrowing


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title', None)
        author = self.request.query_params.get('author', None)
        publication_date = self.request.query_params.get('publication_date', None)

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(authors__name__icontains=author)
        if publication_date:
            queryset = queryset.filter(publication_date=publication_date)

        return queryset

class BorrowBookView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        book = self.get_object()
        if book.copies_available > 0:
            book.copies_available -= 1
            book.save()
            
            BorrowingHistory.objects.create(
                book=book,
                user=request.user,
                borrow_date=timezone.now(),
                status='borrowed'
            )
            return Response({'status': 'Book borrowed successfully'}, status=status.HTTP_200_OK)
        else:
            BorrowPending.objects.create(
                book=book,
                user=request.user,
            )
            return Response({'status':'Book added to reservation'},status=status.HTTP_200_OK)

        return Response({'error': 'No copies available'}, status=status.HTTP_400_BAD_REQUEST)

class ReturnBookView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        book = self.get_object()
        borrowing_history = get_object_or_404(BorrowingHistory, book=book, user=request.user, status='borrowed')
        book.copies_available += 1
        book.save()

        borrowing_history.return_date = timezone.now()
        borrowing_history.status = 'returned'
        borrowing_history.save()

        return Response({'status': 'Book returned successfully'}, status=status.HTTP_200_OK)

class UserBorrowingHistoryView(generics.ListAPIView):
    serializer_class = BorrowingHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BorrowingHistory.objects.filter(user=self.request.user)
    

class CanCreateReview(BasePermission):
    """
    Custom permission to allow users to create a review only if they have returned the book.
    """

    def has_permission(self, request, view):
        # Permission to allow request; general permission check
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if the user has returned the book before writing a review
        returned_history = BorrowingHistory.objects.filter(
            user=request.user, 
            book=obj.book, 
            status='returned'
        ).exists()

        return returned_history

class UserBookReviewCreateView(generics.CreateAPIView):
    queryset = UserBookReview.objects.all()
    serializer_class = UserBookReviewSerializer
    permission_classes = [IsAuthenticated, CanCreateReview]

    def get_object(self):
        # Fetch the Book object that the user is reviewing
        book_id = self.request.data.get('book')
        return Book.objects.get(id=book_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    