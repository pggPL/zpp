import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.serializers import serialize
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app_main.forms import FileUploadForm, ProfileForm, LinkForm1, LinkForm2, ChangePasswordForm
import openpyxl

from app_main.models import Submission, Platform, Profile, SubmissionCategory, ProfileSubmission
from django.core.paginator import Paginator

from app_main.read_file import read_links_file, save_to_db
from app_main.stats import get_categories_dict, get_timechart_data

import json
from django.http import JsonResponse

from app_main.serializers import SubmissionSerializer, ProfileSerializer

from app_main.sorting import Sorting


# decorator – require senior rank
def senior_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.rank == "Senior":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Nie masz uprawnień do wykonania tej akcji")

    return wrapper


def index(request):
    # if user is not logged in, show login screen
    if not request.user.is_authenticated:
        return login_view(request)
    return link_panel_view(request)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return link_panel_view(request)  # Redirect to homepage or other page
        else:
            # Invalid login
            return render(request, 'app_main/login.html', {'error': 'Niepoprawne dane logowania'})
    else:
        return render(request, 'app_main/login.html')


@login_required
def add_file_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                new_data, other_data, new_profile_data, other_profile_data = read_links_file(file)

                context = {
                    'form': form,
                    'new_links_preview': new_data,
                    'other_links_preview': other_data,
                    'new_profile_links_preview': new_profile_data,
                    'other_profile_links_preview': other_profile_data,
                }

                return render(request, "app_main/add_file.html", context)
            except Exception as e:
                context = {
                    'message': 'Plik był niepoprawny.',
                    'form': form,
                }
                return render(request, "app_main/add_file.html", context)
    else:
        form = FileUploadForm()
    return render(request, "app_main/add_file.html", {'form': form})


@login_required
@require_http_methods(["POST"])
def confirm_add_file(request):
    """ This view accepts POST request with the actual data that should be saved in the database """

    try:
        data = json.loads(request.body)
        save_to_db(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'message': 'Data added successfully'}, status=200)


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
        context['links_with_forms'].append({"form": form, "link": link})
    # sort links_with_forms by done
    # context['links_with_forms'].sort(key=lambda x: x['done'])

    # paginacja
    paginator = Paginator(context['links_with_forms'], request.user.get_links_per_page())
    page_number = request.GET.get('page')
    context['links_with_forms'] = paginator.get_page(page_number)

    if not page_number:
        page_number = 1

    context["page_number"] = page_number

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
        'links_without_the_category': len(Submission.objects.filter(category__is_null=True)),
        'links_with_the_category': len(Submission.objects.exclude(category__is_null=True)),
        'most_popular_links': Submission.objects.all().order_by('-report_count')[:5],
        'category_counts': get_categories_dict(),
        'time_history': get_timechart_data()
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
    links = Submission.objects.filter(Q(link__icontains=phrase) | Q(platform__name__icontains=phrase)).order_by('date')
    for link in links:
        link.short_link = link.link[:50] + "..." if len(link.link) > 50 else link.link
    return render(request, 'app_main/lookup.html', {'links': links, 'phrase': phrase})


@login_required
def export_view(request):
    with_categories = (Submission.objects.all().exclude(category__is_null=True))
    with_categories_count = with_categories.count()

    with_categories_not_exported = with_categories.filter(was_exported=False)
    with_categories_not_exported_count = with_categories_not_exported.count()

    profiles = (ProfileSubmission.objects.all())
    profiles_count = profiles.count()

    profiles_not_exported = profiles.filter(was_exported=False)
    profiles_not_exported_count = profiles_not_exported.count()

    return render(request, template_name='app_main/export.html',
        context={
            "with_categories_count": with_categories_count,
            "with_categories_not_exported_count": with_categories_not_exported_count,
            "profiles_count": profiles_count,
            "profiles_not_exported_count": profiles_not_exported_count
        }
    )


@login_required
def export_file_view(request):
    with_categories = (Submission.objects.all().exclude(category__is_null=True)) \
        if request.GET.get("type") == "posts" \
        else (ProfileSubmission.objects.all())

    if request.GET.get("selection") == "all":
        to_export = with_categories
    else:
        to_export = with_categories.filter(was_exported=False)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="links.csv"'
    if request.GET.get("type") == "posts":
        output = "Link,Platforma,Kategoria\n"
        for link in to_export:
            output += f"{link.link},{link.platform.name},{link.category.name}\n"
    else:
        output = "Link,Platforma\n"
        for link in to_export:
            output += f"{link.link},{link.platform.name}\n"

    to_export.update(was_exported=True)
    for link in to_export:
        link.save()

    response.content = output
    return response


@login_required
@require_http_methods(["GET"])
def change_links_per_page_view(request):
    new_count = request.GET.get("new_count")
    request.user.set_links_per_page(new_count)
    return redirect(link_panel_view)


@login_required
@require_http_methods(["GET"])
def get_links_per_page_view(request):
    n_links = request.user.get_links_per_page()
    return JsonResponse({"links_per_page": n_links})


@login_required
@require_http_methods(["GET", "POST"])
def sorting(request):
    if request.method == "GET":
        return JsonResponse(Sorting.get_sorting_types(), safe=False)
    elif request.method == "POST":
        data = json.loads(request.body)
        return JsonResponse("done")


@login_required
@api_view(['GET'])
def search_link_panel_view(request):
    phrase = request.GET.get("phrase")
    links = Submission.objects.filter(Q(link__icontains=phrase) | Q(platform__name__icontains=phrase)).order_by('date')
    serializer = SubmissionSerializer(links, many=True)

    return Response(serializer.data)


@login_required
@api_view(['GET'])
def get_links_on_page_view(request):
    submissions = Sorting.sort(Submission.objects.all(), request.user.sorting)

    page_number = request.GET.get('page')
    links_per_page = request.user.get_links_per_page()

    paginator = Paginator(submissions, links_per_page)
    serializer = SubmissionSerializer(paginator.get_page(page_number), many=True)
    return Response(serializer.data)


@login_required
@api_view(['GET'])
def current_user_view(request):
    serializer = ProfileSerializer(request.user)
    return Response(serializer.data)
