
from django.urls import path

from . import views
from .views import logout_view

urlpatterns = [
    path("", views.index, name="index"),
    path('logout/', logout_view, name='logout'),
    path("accounts_list/", views.accounts_list_view, name="accounts_list"),
    path("edit_account/<int:pk>/", views.edit_account_view, name="edit_account"),
    path("delete_account/<int:pk>/", views.delete_account_view, name="delete_account"),
    path("add_account/", views.add_account_view, name="add_account"),

    path("delete_link/<int:pk>/<str:action>", views.delete_link_view, name="delete_link"),
    path("edit_link/<int:pk>/<str:action>", views.edit_link_view, name="edit_link"),
    path("add_link/<str:action>", views.add_link_view, name="add_link"),
    path("change_password/", views.change_password_view, name="change_password"),
    path("stats/", views.stats_view, name="stats"),
    path("change_category/<int:pk>/<str:category>", views.change_category_view, name="change_category"),
    path("change_category/<int:pk>/", views.remove_category_view, name="remove_category"),
    path("lookup/<str:phrase>", views.lookup_view, name="lookup"),
    path("export/", views.export_view, name="export"),

    # adding input file
    path("add_file/", views.add_file_view, name="add_file"),
    path("confirm_add_file/", views.confirm_add_file, name="confirm_add_file"),

    # link panel
    path("link_panel/", views.link_panel_view, name="link_panel"),
    path("change_links_per_page/", views.change_links_per_page_view, name="change_links_per_page"),
    path("get_links_per_page/", views.get_links_per_page_view, name="get_links_per_page")
]