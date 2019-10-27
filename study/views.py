from django.shortcuts import render, resolve_url, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import TestBook
from .forms import TestBookForm
from django.core.files.storage import FileSystemStorage


def get_result_file(request):
    return render(request, 'study/result.html')


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document'] # html에서 설정한 input name을 key로 file instance 를 받는다
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'study/upload.html', context)


# function based
def book_list(request):
    books = TestBook.objects.all()
    return render(request, 'study/book_list.html', {
        'books': books
    })


def upload_book(request):
    if request.method == 'POST':
        form = TestBookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = TestBookForm()
    return render(request, 'study/upload_book.html',{
        'form': form
    })


# generic class based
class BookListView(ListView):
    model = TestBook
    # template_name = 'book_list.html'
    template_name = 'class_book_list.html'
    context_object_name = 'books'


class UploadBookView(CreateView):
    model = TestBook
    # fields = ('title', 'author', 'pdf', 'cover')
    form_class = TestBookForm
    success_url = reverse_lazy('class_book_list')
    template_name = 'study/upload_book.html'






