from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.BookView.as_view(), name='upload_files'),
    path(r'^result/$', views.get_result_file, name='get_result_file'),
]
