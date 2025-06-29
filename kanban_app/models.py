from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS_CHOICES = [
        ('to_do', 'To do'),
        ('wip', 'Wip'),
        ('on_hold', 'On hold'),
        ('done', 'Done'),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    detail = models.TextField(max_length=400, null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='to_do'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    focused = models.BooleanField(default=False)
    creation_date = models.DateField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title
    

    def toggle_focus(self):
        self.focused = not self.focused
        self.save()
