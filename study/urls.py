from django.urls import path, include
from . import views
urlpatterns = [
    path(r'^result/$', views.get_result_file, name='get_result_file'),
    path('upload/', views.upload, name='upload'),
    path('books/', views.book_list, name='book_list'),
    path('books/upload/', views.upload_book, name='upload_book'),
    path('class/books/', views.BookListView.as_view(), name='class_book_list'),
    path('class/books/upload', views.UploadBookView.as_view(), name='class_upload_book'),
]
