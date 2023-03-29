from django.contrib.auth.models import User
from django.db import models

class Libro(models.Model):

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    genre = models.CharField(max_length=100)
    pages = models.IntegerField()

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Libro, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    score = models.IntegerField()

    def __str__(self):
        return self.content