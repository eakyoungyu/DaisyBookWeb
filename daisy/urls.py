from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.BookView.as_view(), name='upload_files'),
    path('result/', views.result_file, name='result_file'),
    path('celery/', views.celery, name='celery'),
    path('celery_bar/', views.celery_bar, name='celery_bar'),
]
