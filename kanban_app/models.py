from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils.html import format_html


class Task(models.Model):
    STATUS_CHOICES = [
        ('to_do', 'To do'),
        ('wip', 'Wip'),
        ('on_hold', 'On hold'),
        ('done', 'Done'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    detail = models.TextField(max_length=600, null=True, blank=True)
    priority = models.CharField(
        max_length=100,
        choices=PRIORITY_CHOICES,
        default='low'
    )
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default='to_do'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True, editable=False)


    def __str__(self):
        return self.title
    

    def get_days_left(self):
        priority_days = {
            'low': 14,
            'medium': 7,
            'high': 2,
        }
        max_days = priority_days.get(self.priority, 7)
        days_passed = (date.today() - self.creation_date).days
        days_remaining = max_days - days_passed

        if days_remaining >= 2:
            message = f"{days_remaining} days left"
        elif days_remaining == 1:
            message = f"{days_remaining} day left"
        elif days_remaining == 0:
            message = "Expires today"
        elif days_remaining == -1:
            message = format_html(
                '<span class="text-red-600">Expired {} day ago</span>',
                abs(days_remaining)
            )
        else:
            message = format_html(
                '<span class="text-red-600">Expired {} days ago</span>',
                abs(days_remaining)
            )
        return message


    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['priority', 'status', '-creation_date']
