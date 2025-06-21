from django.contrib import admin
from .models import Task
from django.contrib.sessions.models import Session


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'detail', 'status')
    search_fields = ('id', 'title', 'detail', 'status')


admin.site.register(Session)
admin.site.register(Task, TaskAdmin)
