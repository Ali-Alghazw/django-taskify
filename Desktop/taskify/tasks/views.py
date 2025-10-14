from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from .forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def task_list(request):
    filter_status = request.GET.get('filter', 'all')
    sort_option = request.GET.get('sort', 'due_date')
    search_query = request.GET.get('q', '')

    tasks = Task.objects.filter(user=request.user)

    # 🔍 Search filter
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # ✅ Status filter
    if filter_status == 'completed':
        tasks = tasks.filter(is_completed=True)
    elif filter_status == 'pending':
        tasks = tasks.filter(is_completed=False)

    # 🧭 Sorting
    if sort_option == 'title':
        tasks = tasks.order_by('title')
    else:
        tasks = tasks.order_by('due_date')

    # 📄 Pagination
    paginator = Paginator(tasks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'filter_status': filter_status,
        'sort_option': sort_option,
        'search_query': search_query,
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task added successfully.")
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.info(request, "Task updated.")
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.warning(request, "Task deleted.")
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    messages.success(request, "Task status changed.")
    return redirect('task_list')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def toggle_task_completion(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    return redirect('task_list')