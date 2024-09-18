from django.contrib import admin
from django.urls import include, path
from .views import BookListCreateView, BookRetrieveUpdateDestroyView, BorrowingHistoryListView

urlpatterns = [
    path('list', BookListCreateView.as_view(), name='book-list-create'),
    path('<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-retrieve-update-delete'),
    path('borrowing/', BorrowingHistoryListView.as_view(), name='borrowing-history-list'),
   
]