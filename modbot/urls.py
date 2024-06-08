
from django.urls import path

from modbot import views

urlpatterns = [
    path("run/", views.run_bot, name="run_bot"),


]