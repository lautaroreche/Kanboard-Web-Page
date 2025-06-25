from django.contrib import admin
from .models import Task
from django.contrib.sessions.models import Session


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'detail', 'status', 'user', 'creation_date', 'focused')
    search_fields = ('id', 'title', 'detail', 'status', 'user', 'creation_date', 'focused')


admin.site.register(Session)
admin.site.register(Task, TaskAdmin)
