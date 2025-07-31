from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, IntegerField



def get_initial_context(user):
    to_do_tasks = []
    wip_tasks = []
    on_hold_tasks = []
    done_tasks = []

    tasks = Task.objects.filter(user=user).annotate(
        priority_order=Case(
            When(priority='high', then=0),
            When(priority='medium', then=1),
            When(priority='low', then=2),
            default=3,
            output_field=IntegerField()
        )
    ).order_by('priority_order', 'id')
    
    for task in tasks:
        if task.status == 'to_do':
            to_do_tasks.append(task)
        elif task.status == 'wip':
            wip_tasks.append(task)
        elif task.status == 'on_hold':
            on_hold_tasks.append(task)
        elif task.status == 'done':
            done_tasks.append(task)

    columns = [
        {"name": 'TO DO', "status": 'to_do', "tasks": to_do_tasks},
        {"name": 'WIP', "status": 'wip',"tasks": wip_tasks},
        {"name": 'ON HOLD', "status": 'on_hold', "tasks": on_hold_tasks},
        {"name": 'DONE', "status": 'done', "tasks": done_tasks},
    ]
    context = {
        "columns": columns,
    }
    return context


@login_required
def home(request):
    context = get_initial_context(request.user)
    return render(request, 'index.html', context)


@login_required
def modify_status(request, task_id, new_status):
    task = Task.objects.get(id=task_id, user=request.user)
    task.status = new_status
    task.save()
    return redirect('home')


@login_required
def create(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        detail = request.POST.get("detail").strip()
        priority = request.POST.get("priority").strip()
        status = request.POST.get("status").strip()
        Task.objects.create(title=title, detail=detail, priority=priority, status=status, user=request.user)
    return redirect("home")


@login_required
def edit(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    if request.method == "POST":
        task.title = request.POST.get("title", "").strip()
        task.detail = request.POST.get("detail", "").strip()
        task.priority = request.POST.get("priority", "").strip()
        task.status = request.POST.get("status", "").strip()
        task.save()
        return redirect('home')


@login_required
def delete(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    return redirect('home')
