from django.shortcuts import render

# index.html


def index(request):
    # if user is not logger, show login screen
    if not request.user.is_authenticated:
        return render(request, "app_main/login.html")
    return main_panel_view(request)

def login_view(request):
    return render(request, "app_main/login.html")

def main_panel_view(request):
    return render(request, "app_main/main_panel.html")

def add_file_view(request):
    return render(request, "app_main/add_file.html")