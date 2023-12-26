from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


# index.html


def index(request):
    # if user is not logger, show login screen
    if not request.user.is_authenticated:
        return login_view(request)
    return main_panel_view(request)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return main_panel_view(request)  # Redirect to homepage or other page
        else:
            # Invalid login
            return render(request, 'app_main/login.html', {'error': 'Niepoprawne dane logowania'})
    else:
        return render(request, 'app_main/login.html')

def main_panel_view(request):
    return render(request, "app_main/main_panel.html")

def add_file_view(request):
    return render(request, "app_main/add_file.html")

def logout_view(request):
    logout(request)
    return redirect("index")