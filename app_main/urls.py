
from django.urls import path

from . import views
from .views import logout_view

urlpatterns = [
    path("", views.index, name="index"),
    path('logout/', logout_view, name='logout'),
    path("add_file/", views.add_file_view, name="add_file"),
    path("accounts_list/", views.accounts_list_view, name="accounts_list"),
    path("edit_account/<int:pk>/", views.edit_account_view, name="edit_account"),
    path("delete_account/<int:pk>/", views.delete_account_view, name="delete_account"),
    path("add_account/", views.add_account_view, name="add_account"),
]