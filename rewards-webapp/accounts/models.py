from django.db import models
from django.contrib.auth.models import User

# # Create your models here.
# #user = User.objects.create_user('username', 'email', 'password')

class Customer(User):
    pass
    # username = models.CharField(max_length = 50)
    # PAPERBACK = 2
    # EBOOK = 3
    # BOOK_TYPES = (
    #     (HARDCOVER, 'Hardcover'),
    #     (PAPERBACK, 'Paperback'),
    #     (EBOOK, 'E-book'),
    # )
    # title = models.CharField(max_length=50)
    # publication_date = models.DateField(null=True)

    # timestamp = models.DateField(auto_now_add=True, auto_now=False)
