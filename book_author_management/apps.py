from django.apps import AppConfig


class BookAuthorManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'book_author_management'

    def ready(self):
        import book_author_management.signals
