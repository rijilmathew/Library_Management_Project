from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import BorrowingHistory, BorrowPending

@receiver(post_save, sender=BorrowingHistory)
def notify_user_on_return(sender, instance, **kwargs):
    if instance.status == 'returned':
        book = instance.book
        # Check if there are pending requests for the book
        pending_request = BorrowPending.objects.filter(book=book, status='pending').first()

        if pending_request:
            user = pending_request.user
            # Return or log a response-like message
            response_message = f"Hello {user.username}, the book '{book.title}' is now available for borrowing."
            
            # Here you could log the message, send it to a notification system, or handle it otherwise.
            print(response_message)  # For development purposes, you can log the response
            return response_message
        return None