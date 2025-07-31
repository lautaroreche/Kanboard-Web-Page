from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.decorators import login_required


def get_initial_context(user):
    to_do_tasks = []
    wip_tasks = []
    on_hold_tasks = []
    done_tasks = []

    tasks = Task.objects.filter(user=user).order_by('id')
    
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
def change_status(request, task_id, direction):
    task = Task.objects.get(id=task_id, user=request.user)

    status_flow = ["to_do", "wip", "on_hold", "done"]

    try:
        current_index = status_flow.index(task.status)
        if direction == "next" and current_index < len(status_flow) - 1:
            task.status = status_flow[current_index + 1]
        elif direction == "prev" and current_index > 0:
            task.status = status_flow[current_index - 1]
        task.save()
    except ValueError:
        pass
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
