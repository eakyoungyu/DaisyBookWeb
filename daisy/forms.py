from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    text_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Book
        fields = ('name', 'start_page', 'end_page', 'is_poem')
