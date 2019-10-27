from django import forms
from .models import Book, TestBook


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('name', 'start_page')


class TestBookForm(forms.ModelForm):
    class Meta:
        model = TestBook
        fields = ('title', 'author', 'pdf', 'cover')
