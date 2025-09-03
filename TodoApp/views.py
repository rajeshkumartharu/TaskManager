from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from .models import TasksModel
from .forms import TaskForm

def landing_page_view(request):
    return render(request, "landingpage.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Passwords do not match!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully!")
            return redirect("login")
    
    return render(request, "register.html")  # <-- just the filename

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

@login_required
def dashboard_view(request):
    user = request.user

    # Fetch all tasks for the logged-in user
    all_tasks = TasksModel.objects.filter(user=user).order_by('-created_at')
    pending_list = all_tasks.filter(status='pending')
    completed_list = all_tasks.filter(status='complete')

    # Stats
    total_tasks = all_tasks.count()
    pending_tasks = pending_list.count()
    completed_tasks = completed_list.count()

    context = {
        'user': user,
        'all_tasks': all_tasks,
        'pending_list': pending_list,
        'completed_list': completed_list,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
    }

    return render(request, 'dashboard.html', context)


@login_required
def create_task_view(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        status = 'complete' if request.POST.get('status') == 'complete' else 'pending'

        if not title:
            messages.error(request, "Task title is required.")
            return render(request, 'create_task.html')

        # Create the task
        TasksModel.objects.create(
            user=request.user,
            title=title,
            description=description,
            due_date=due_date if due_date else None,
            status=status
        )

        messages.success(request, "Task created successfully!")
        return redirect('dashboard')  # Make sure 'dashboard' exists in urls.py

    return render(request, 'create_task.html')


@login_required
def task_update_view(request, task_id):
    # Get the task object for the logged-in user
    task = get_object_or_404(TasksModel, pk=task_id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)  # bind POST data to the existing task
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect after successful update
    else:
        form = TaskForm(instance=task)  # pre-fill the form with existing task data

    return render(request, 'task_update.html', {'form': form})

# ----------------------
# Delete Task
# ----------------------
@login_required
def task_delete_view(request, task_id):
    task = get_object_or_404(TasksModel, id=task_id, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')  # redirect to dashboard or task list

    return render(request, 'task_delete.html', {'task': task})

@login_required
def logout_confirm_view(request):
    """Show logout confirmation page"""
    return render(request, 'logout.html')

@login_required
def logout_view(request):
    """Log out user and redirect"""
    if request.method == "POST":
        logout(request)
        return redirect('landingpage')  # Replace 'login' with your login URL name
    return redirect('dashboard')  # If user accesses logout_view directly
