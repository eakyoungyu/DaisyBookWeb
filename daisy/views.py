from django.shortcuts import render, resolve_url, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .models import Book
from .forms import BookForm
from django.core.files.storage import FileSystemStorage
import os


def make_success_url(url, book_name):
    url += '?'
    url += 'book_name='
    url += book_name
    return url


class BookView(FormView):
    model = Book
    form_class = BookForm
    template_name = 'daisy/main.html'
    success_url = reverse_lazy('get_result_file')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('text_files')
        book_name = request.POST['name']
        print('DATE', self.model.created_on)
        print(book_name)
        if form.is_valid():
            fs = FileSystemStorage()
            for f in files:
                name = fs.save(os.path.join(book_name, f.name), f)
            self.success_url = make_success_url(self.get_success_url(), book_name)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def get_result_file(request):
    context = {'book_name': request.GET['book_name']}
    return render(request, 'daisy/result.html', context)





