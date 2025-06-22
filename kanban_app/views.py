from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.decorators import login_required


def get_context(user):
    to_do_tasks = []
    wip_tasks = []
    on_hold_tasks = []
    done_tasks = []

    tasks = Task.objects.filter(user=user)
    
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
    context = get_context(request.user)
    return render(request, 'index.html', context)


@login_required
def change_status(request, task_id, direction):
    task = Task.objects.get(id=task_id, user=request.user)

    if direction == "next":
        if task.status == "on_hold":
            task.status = "done"
        if task.status == "wip":
            task.status = "on_hold"
        if task.status == "to_do":
            task.status = "wip"
    if direction == "prev":
        if task.status == "wip":
            task.status = "to_do"
        if task.status == "on_hold":
            task.status = "wip"
        if task.status == "done":
            task.status = "on_hold"
    task.save()
    return redirect('home')


@login_required
def edit(request, task_id):
    return redirect('home')


@login_required
def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        detail = request.POST.get("detail")
        Task.objects.create(title=title, detail=detail, status="to_do", user=request.user)
    return redirect("home")


@login_required
def delete(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    return redirect('home')