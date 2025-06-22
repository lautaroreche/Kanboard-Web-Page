from django.shortcuts import render, redirect
from .models import Task


def get_context():
    to_do_tasks = []
    wip_tasks = []
    on_hold_tasks = []
    done_tasks = []

    tasks = Task.objects.all()
    
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


def home(request):
    context = get_context()
    return render(request, 'index.html', context)


def change_status(request, id, direction):
    task = Task.objects.get(id=id)

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
        
        
        
