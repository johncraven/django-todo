# tasks/models.py
from django.db import models
from django.urls import reverse
from datetime import datetime


class Task(models.Model):
    class Priority(models.TextChoices):
        HIGH = "1", "‼️ High"
        MED = "2", "❗️ Medium"
        LOW = "3", "〰️ Low"

    title = models.CharField(max_length=50, null=False)
    is_complete = models.BooleanField(default=False, null=False)
    author = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, related_name="tasks", default=""
    )
    description = models.TextField(null=False, blank=True, default="")
    due_on = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    priority = models.CharField(
        null=False, blank=True, choices=Priority.choices, default=Priority.LOW
    )

    modified_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if len(self.title) < 31 else self.title[:30] + "..."

    def get_absolute_url(self):
        return reverse("task_detail", kwargs={"pk": self.pk})

    def is_past_due(self):
        if not self.due_on:
            return False
        else:
            return self.due_on < datetime.now().date()


class Comment(models.Model):
    author = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, related_name="comments"
    )
    task = models.ForeignKey(
        "tasks.Task", on_delete=models.CASCADE, related_name="comments"
    )
    body = models.TextField(null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
