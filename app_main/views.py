from django.shortcuts import render

# index.html


def index(request):
    return render(request, "app_main/index.html")