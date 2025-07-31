from django.contrib import admin
from .models import Task
from django.contrib.sessions.models import Session


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'detail', 'priority', 'status', 'user', 'creation_date')
    search_fields = ('id', 'title', 'detail', 'priority', 'status', 'user', 'creation_date')
    list_filter = ('priority', 'status', 'user', 'creation_date')


admin.site.register(Session)
admin.site.register(Task, TaskAdmin)
