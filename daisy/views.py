from django.shortcuts import render
from django.views.generic.edit import FormView
from django.http import HttpResponse
from .models import Book, Images
from .forms import BookForm
from .forms import UploadForm


def index(request):
    return render(request, 'daisy/main.html')


class FileFieldView(FormView):
    form_class = UploadForm
    template_name = 'main.html'
    success_url = 'result.html'

    def post(self, request, *args, **kargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                f.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def upload_files(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print('saved file')
        else:
            print('invalid')
    return render(request, 'daisy/main.html', {'form': form})

# def upload_files(request):
#     if request.method == 'POST':
#         form = UploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             print('saved file')
#         else:
#             print('invalid')
#     return render(request, 'daisy/main.html', locals())