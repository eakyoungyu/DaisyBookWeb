from django.shortcuts import render, resolve_url, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

from .models import Book
from .forms import BookForm
from django.views.generic.edit import FormView
from django.views.generic import TemplateView

import os
import shutil


from webapp.settings import BOOK_ROOT, BOOK_URL, MEDIA_ROOT
from .task import sleepy, my_task, make_book_async
from .image_to_text import make_book
from celery.result import AsyncResult


def make_success_url(url, book_name):
    url += '?'
    url += 'book_name='
    url += book_name
    return url


class BookView(FormView):
    model = Book
    form_class = BookForm
    template_name = 'daisy/main.html'
    success_url = reverse_lazy('result_file')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        files = request.FILES.getlist('text_files')
        book_name = request.POST['name']
        start_page = request.POST['start_page']
        end_page = request.POST['end_page']

        if form.is_valid():
            book_dir = os.path.join(MEDIA_ROOT, book_name)
            if os.path.isdir(book_dir):
                shutil.rmtree(book_dir)

            fs = FileSystemStorage()
            for f in files:
                name = fs.save(os.path.join(book_name, f.name), f)

            #     async task with celery
            # result = make_book_async.delay(book_name, start_page, end_page)
            # self.success_url = reverse('celery_bar') + '?task_id=' + result.task_id

            # making book after saving all files
            self.success_url = make_success_url(self.get_success_url(), book_name)
            make_book(book_name, start_page, end_page)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def make_book_path(book_name):
    return BOOK_URL+book_name+'.txt'


def result_file(request):
    context = {'book_name': request.GET['book_name']}
    context['result_file_path'] = make_book_path(context['book_name'])
    print(context['result_file_path'])
    return render(request, 'daisy/result.html', context)


# def progress_view(request):
#     second = 10
#     result = my_task.delay()
#     # result = sleepy.delay(1)
#     return render(request, 'daisy/display_progress.html', context={'task_id': result.task_id, 'static': static})


def celery(request):
    result = my_task.delay()
    return redirect(reverse('celery_bar')+'?task_id='+result.task_id)


def celery_bar(request):
    context = {'task_id': request.GET['task_id']}
    print('ID!!!!!!!!!!!!!!!!!!!!!!', context['task_id'])
    return render(request, 'daisy/display_progress.html', context)

