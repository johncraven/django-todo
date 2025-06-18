# tasks/models.py
from django.db import models
from django.urls import reverse


class Task(models.Model):
    title = models.CharField(max_length=50, null=False)
    is_complete = models.BooleanField(default=False, null=False)
    author = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, related_name="tasks", default=""
    )

    def __str__(self):
        return self.title if len(self.title) < 31 else self.title[:30] + "..."

    def get_absolute_url(self):
        return reverse("task_detail", kwargs={"pk": self.pk})
