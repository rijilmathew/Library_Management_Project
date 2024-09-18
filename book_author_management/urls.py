from django.contrib import admin
from django.urls import include, path
from .views import *

urlpatterns = [
    path('book-list/', BookListCreateView.as_view(), name='book-list-create'),
    path('book/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-retrieve-update-delete'),
    path('borrowing/', BorrowingHistoryListView.as_view(), name='borrowing-history-list'),
    path('authors/', AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', AuthorRetrieveUpdateDestroyView.as_view(), name='author-retrieve-update-delete'),

    path('list-books/', BookListView.as_view(), name='book-list'),
    path('book/<int:pk>/borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('book/<int:pk>/return/', ReturnBookView.as_view(), name='return-book'),
    path('my-borrowing/', UserBorrowingHistoryView.as_view(), name='user-borrowing-history'),
   
]


