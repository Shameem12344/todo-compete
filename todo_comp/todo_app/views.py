from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator
from .models import User, Task, UserProfile
from datetime import datetime

def index(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    else:
        return HttpResponseRedirect(reverse("login"))

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "todo_app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "todo_app/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "todo_app/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            UserProfile.objects.create(user=user)
        except IntegrityError as e:
            return render(request, "todo_app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "todo_app/register.html")

@login_required
def task_list(request):
    today = timezone.now().date()
    tasks = Task.objects.filter(user=request.user, created_at__date=today)

    if request.method == 'POST':
        if 'title' in request.POST:
            if tasks.count() < 5:
                Task.objects.create(user=request.user, title=request.POST['title'])
        elif 'task_id' in request.POST:
            task = Task.objects.get(id=request.POST['task_id'], user=request.user)
            task.completed = True
            task.completion_date = today  # Ensure the completion date is set to today
            task.save()
            profile = request.user.userprofile
            profile.gems += 1
            profile.save()
        return redirect('task_list')

    return render(request, 'todo_app/task_list.html', {'tasks': tasks})

@login_required
def profile_view(request, username):
    user = User.objects.get(username=username)
    today = timezone.now().date()
    completed_tasks = Task.objects.filter(user=user, completed=True).order_by('-completion_date')
    pending_tasks_today = Task.objects.filter(user=user, completed=False, created_at__date=today)
    all_tasks_today = Task.objects.filter(user=user, created_at__date=today)
    tasks_left_today = 5 - all_tasks_today.count()
    paginator = Paginator(completed_tasks, 10)  # Show 10 tasks per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Group tasks by date
    grouped_tasks = {}
    for task in completed_tasks:
        date = task.completion_date
        if date not in grouped_tasks:
            grouped_tasks[date] = {'completed': [], 'pending': []}
        grouped_tasks[date]['completed'].append(task)

    for task in pending_tasks_today:
        date = task.created_at.date()
        if date not in grouped_tasks:
            grouped_tasks[date] = {'completed': [], 'pending': []}
        grouped_tasks[date]['pending'].append(task)

    return render(request, 'todo_app/profile.html', {
        'profile_user': user,
        'grouped_tasks': grouped_tasks,
        'tasks_left_today': tasks_left_today,
        'gems': user.userprofile.gems,
        'page_obj': page_obj,
    })

@login_required
def tasks_by_date(request, username, date):
    user = User.objects.get(username=username)
    date = datetime.strptime(date, '%Y-%m-%d').date()
    completed_tasks = Task.objects.filter(user=user, completion_date=date, completed=True)
    pending_tasks = Task.objects.filter(user=user, created_at__date=date, completed=False)

    return render(request, 'todo_app/tasks_by_date.html', {
        'profile_user': user,
        'date': date,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
    })
