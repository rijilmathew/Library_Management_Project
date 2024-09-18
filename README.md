# Library_Management_Project
The Library Management System is a Django-based web application designed to manage books, authors, and borrowing histories. It provides functionality for adding, updating, and deleting books, as well as tracking borrowing activities. This project uses Django REST Framework for building APIs and PostgreSQL as the database.



#Features

Book Management: Add, update, and delete books.

Author Management: Add and view authors.

Borrowing History: Track borrowing and returning of books.

User Management: Role-based access for staff and regular users.


#Requirements


asgiref==3.8.1

Django==5.1.1

django-cors-headers==4.4.0

djangorestframework==3.15.2

djangorestframework-simplejwt==5.3.1

pillow==10.4.0

psycopg2-binary==2.9.9

PyJWT==2.9.0

python-dotenv==1.0.1

sqlparse==0.5.1

tzdata==2024.1



1 Clone the Repository

2 Create a Virtual Environment

Install Dependencies

pip install -r requirements.txt

API Endpoints

Book Management Endpoints

Add Books (POST /api/books/book-list): Add new books to the library.

Update Books (PUT /api/books/book/{id}/): Update book information.

Delete Books (DELETE /api/books/books/{id}/): Delete books.

View All Borrowing Histories (GET /api/books/borrowing/): View all borrowing history records.

Author Management Endpoints

Add Authors (POST /api/books/authors/): Add new authors to the system.

List Authors (GET /api/authors/): Retrieve a list of all authors



