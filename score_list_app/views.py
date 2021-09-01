from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from .forms import TodoForm, UploadForm, UploadFileForm
from .models import ToDo, ScoreList
from django.utils import timezone
from django.http import HttpResponseRedirect
import pandas as pd
import numpy as np


def home(request):
    return render(request, 'score_list_app/home.html')


# Create your views here.
def signup_user(request):
    if request.method == 'GET':
        return render(request, 'score_list_app/signup_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('score_list')
            except IntegrityError:
                return render(request, 'score_list_app/signup_user.html',
                              {'form': UserCreationForm(), 'Error': 'This username have been chosen before'})
        else:
            return render(request, 'score_list_app/signup_user.html',
                          {'form': UserCreationForm(), 'Error': 'Password mismatch'})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'score_list_app/login_user.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'score_list_app/login_user.html',
                          {'form': AuthenticationForm(), 'Error': 'This username and password does not match'})
        else:
            login(request, user)
            return redirect('score_list')


@login_required
def profile(request):
    todos = ToDo.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'score_list_app/profile.html', {'todos': todos})


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def create_todo(request):
    if request.method == 'GET':
        return render(request, 'score_list_app/create_todo.html', {'form': TodoForm()})
    else:
        form = TodoForm(request.POST)
        new_todo = form.save(commit=False)
        new_todo.user = request.user
        new_todo.save()
        return redirect('score_list')


@login_required
def todo_view(request, todo_pk):
    selected_todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    form = TodoForm(instance=selected_todo)
    if request.method == 'GET':
        return render(request, 'score_list_app/todo_view.html', {'selected_todo': selected_todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=selected_todo)
            form.save()
            return redirect('score_list')
        except ValueError:
            return render(request, 'score_list_app/todo_view.html',
                          {'selected_todo': selected_todo, 'form': form, 'error': 'Bad value!'})


@login_required
def complete_task(request, todo_pk):
    if request.method == 'POST':
        selected_todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
        selected_todo.date_completed = timezone.now()
        selected_todo.save()
        return redirect('profile')


@login_required
def delete_task(request, todo_pk):
    if request.method == 'POST':
        selected_todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
        selected_todo.delete()
        return redirect('profile')


@login_required
def completed(request):
    todos = ToDo.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'score_list_app/completed.html', {'todos': todos})


@login_required
def upload_file(request):
    if request.method == 'GET':
        return render(request, 'score_list_app/upload_file.html', {'form': UploadFileForm()})
    else:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # myfile = request.FILES['file']
            # file = pd.read_csv(myfile.temporary_file_path)
            try:
                df = pd.read_csv(request.FILES['file'])
                gt = pd.read_csv(staticfiles_storage.path('score_list_app/gt.csv'))
                n_samples = gt.shape[0]

                rmse_value = np.sqrt(np.sum((df['SalePrice'].values - gt['SalePriceGT'].values) ** 2)) / n_samples

                user_old_score = ScoreList.objects.filter(user=request.user)
                user_old_score.delete()

                score = ScoreList(score_project1=rmse_value, user=request.user)
                score.save()

                return redirect('score_list')
            except KeyError:
                return render(request, 'score_list_app/upload_file.html',
                              {'form': UploadFileForm(), 'Error': 'Wrong file format!'})
            except ValueError:
                return render(request, 'score_list_app/upload_file.html',
                              {'form': UploadFileForm(), 'Error': 'Values should be according to submission file. Wrong file format!'})
        else:
            return render(request, 'score_list_app/upload_file.html',
                          {'form': UploadFileForm(), 'Error': 'Wrong file format!'})


def score_list(request):
    scores = ScoreList.objects.all().order_by('score_project1')
    return render(request, 'score_list_app/score_list.html', {'scores': scores})
