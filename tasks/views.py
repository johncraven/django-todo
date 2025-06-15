from django.shortcuts import render
from django.views.generic import DetailView, DeleteView, UpdateView


from .models import Task


def homepage_view(request):
    tasks = Task.objects.all().order_by("is_complete")
    return render(
        request,
        template_name="home.html",
        context={
            "tasks": tasks,
        },
    )


class TaskDetail(DetailView):
    model = Task
    context_object_name = "task"
