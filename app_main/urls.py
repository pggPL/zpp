
from django.urls import path

from . import views
from .views import logout_view

urlpatterns = [
    path("", views.index, name="index"),
    path('logout/', logout_view, name='logout'),
    path("add_file/", views.add_file_view, name="add_file"),
]