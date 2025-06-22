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
    title = models.CharField(max_length=200)
    detail = models.TextField(max_length=1000)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='to_do'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
