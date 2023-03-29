from django import forms
from .models import Libro, Review

class BookForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['title', 'author', 'genre', 'pages']



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'score']
