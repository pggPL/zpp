from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from app_main.forms import FileUploadForm, ProfileForm
import openpyxl

from app_main.models import Submission, Platform, Profile
from django.core.paginator import Paginator



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
    links_list = Submission.objects.all()
    
    # Paginacja
    paginator = Paginator(links_list, 30)  # 10 linków na stronę
    page_number = request.GET.get('page')
    links = paginator.get_page(page_number)
    
    # Skracanie linku
    for link in links:
        link.short_link = link.link[:50] + "..." if len(link.link) > 50 else link.link
    
    return render(request, "app_main/main_panel.html", context={'links': links})

def add_file_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            workbook = openpyxl.load_workbook(file)
            worksheet = workbook.active

            data = []
            for row in worksheet.iter_rows(min_row=2, max_col=2, values_only=True):
                platform, link = row
                
                platform = Platform.objects.get_or_create(name=platform)[0]
                
                # create link in database
                Submission.objects.get_or_create(link=link, platform=platform)

            return render(request, "app_main/add_file.html", {'form': form, 'message': 'Plik został dodany'})
    else:
        form = FileUploadForm()
    return render(request, "app_main/add_file.html", {'form': form})

def logout_view(request):
    logout(request)
    return redirect("index")

def accounts_list_view(request):
    context = {
        'users': Profile.objects.all()
    }
    return render(request, "app_main/accounts.html", context=context)

def edit_account_view(request, pk):
    obiekt = get_object_or_404(Profile, pk=pk)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=obiekt)
        if form.is_valid():
            form.save()
            return redirect('accounts_list')
    else:
        form = ProfileForm(instance=obiekt)
    return render(request, 'app_main/form.html', {'form': form, 'name': 'Edytuj konto'})

def delete_account_view(request, pk):
    # delete if there is no object connected to this account
    account = get_object_or_404(Profile, pk=pk)
    # if this is current user, logout
    if account == request.user:
        return HttpResponse("Nie możesz usunąć swojego konta")
    account.delete()
    return redirect('accounts_list')

def add_account_view(request):
    info_message = "Na podany adres email zostanie wysłane zaproszenie do rejestracji."
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts_list')
    else:
        form = ProfileForm()
    return render(request, 'app_main/form.html',
                  {'form': form, 'name': 'Dodaj konto', 'back_link': 'accounts_list', 'info': info_message})