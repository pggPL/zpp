import os

from django.contrib.auth import authenticate, login, logout
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from app_main.forms import FileUploadForm, ProfileForm, LinkForm1, LinkForm2, ChangePasswordForm
import openpyxl

from app_main.models import Submission, Platform, Profile, SubmissionCategory
from django.core.paginator import Paginator
from selenium import webdriver


# decorator – require senior rank
def senior_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.rank == "Senior":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Nie masz uprawnień do wykonania tej akcji")
    return wrapper



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

@login_required
def main_panel_view(request):
    links_list = Submission.objects.all().order_by('link')
    
    # Paginacja
    paginator = Paginator(links_list, 30)  # 10 linków na stronę
    page_number = request.GET.get('page')
    links = paginator.get_page(page_number)
    
    # Skracanie linku
    for link in links:
        link.short_link = link.link[:50] + "..." if len(link.link) > 50 else link.link
    
    return render(request, "app_main/main_panel.html", context={'links': links})

@login_required
def add_file_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            workbook = openpyxl.load_workbook(file)
            worksheet = workbook.active
            
            total_links = worksheet.max_row - 1
            total_unique_links = 0

            for row in worksheet.iter_rows(min_row=2, max_col=2, values_only=True):
                platform, link = row
                
                # check if link already exists in database
                if Submission.objects.filter(link=link).exists():
                    continue
                total_unique_links += 1
                
                platform = Platform.objects.get_or_create(name=platform)[0]
                
                # create link in database
                Submission.objects.get_or_create(link=link, platform=platform)
            
            context = {
                'total_links': total_links,
                'total_unique_links': total_unique_links,
                'message': 'Plik został dodany. ',
                'form': form
            }

            return render(request, "app_main/add_file.html", context)
    else:
        form = FileUploadForm()
    return render(request, "app_main/add_file.html", {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("index")

@senior_required
def accounts_list_view(request):
    context = {
        'users': Profile.objects.all()
    }
    return render(request, "app_main/accounts.html", context=context)

@senior_required
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

@senior_required
def delete_account_view(request, pk):
    # delete if there is no object connected to this account
    account = get_object_or_404(Profile, pk=pk)
    # if this is current user, logout
    if account == request.user:
        return HttpResponse("Nie możesz usunąć swojego konta")
    account.delete()
    return redirect('accounts_list')

@senior_required
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

@login_required
def link_panel_view(request):
    context = {
        'links_with_forms': []
    }
    
    submissions = Submission.objects.all()

    for link in submissions:
        link.short_link = link.link[:30] + "..." if len(link.link) > 30 else link.link
    
    for link in submissions:
        form = LinkForm1(instance=link)
        context['links_with_forms'].append({"form": form, "link": link, "done": link.category is not None})
    # sort links_with_forms by done
    context['links_with_forms'].sort(key=lambda x: x['done'])
        
    return render(request, "app_main/link_panel.html", context=context)

@login_required
def delete_link_view(request, pk, action):
    link = get_object_or_404(Submission, pk=pk)
    link.delete()
    return redirect(action)

@login_required
def edit_link_view(request, pk, action):
    obiekt = get_object_or_404(Submission, pk=pk)
    if request.method == "POST":
        form = LinkForm2(request.POST, instance=obiekt)
        if form.is_valid():
            form.save()
            return redirect(action)
    else:
        form = LinkForm2(instance=obiekt)
    return render(request, 'app_main/form.html', {'form': form, 'name': 'Edytuj link'})

@login_required
def add_link_view(request, action):
    if request.method == "POST":
        form = LinkForm2(request.POST)
        if form.is_valid():
            form.save()
            return redirect(action)
    else:
        form = LinkForm2()
    return render(request, 'app_main/form.html', {'form': form, 'name': 'Dodaj link'})

@login_required
def change_password_view(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'app_main/form.html', {'form': form, 'name': 'Zmień hasło'})

@login_required
def stats_view(request):
    context = {
        'links_number': len(Submission.objects.all()),
        'links_without_the_cathegory': len(Submission.objects.filter(category=None)),
        'links_with_the_cathegory': len(Submission.objects.exclude(category=None)),
    }
    return render(request, 'app_main/stats.html', context=context)

@login_required
def change_category_view(request, pk, category):
    link = get_object_or_404(Submission, pk=pk)
    link.category = SubmissionCategory.objects.get(id=category)
    link.save()
    return HttpResponse("done")


@login_required
def remove_category_view(request, pk):
    link = get_object_or_404(Submission, pk=pk)
    link.category = None
    link.save()
    return HttpResponse("not done")


@login_required
def lookup_view(request, phrase):
    links = Submission.objects.filter(Q(link__icontains=phrase) | Q(platform__name__icontains=phrase)).order_by('link')
    for link in links:
        link.short_link = link.link[:50] + "..." if len(link.link) > 50 else link.link
    return render(request, 'app_main/lookup.html', {'links': links, 'phrase': phrase})


@login_required
def export_view(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="links.txt"'
    
    output = ""
    for link in Submission.objects.all():
        if link.category is not None and link.category is not None:
            output += link.link + "(" + link.platform.name + ", " + link.category.name + ")\n"
    response.content = output
    
    return response