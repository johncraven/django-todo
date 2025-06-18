# tasks/views.py
from django.shortcuts import render
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import Task
from .forms import TaskUpdateForm

#


@login_required
def homepage_view(request):
    tasks = Task.objects.filter(author=request.user).order_by("is_complete")
    return render(
        request,
        template_name="home.html",
        context={
            "tasks": tasks,
        },
    )


class TaskCreate(CreateView):
    model = Task
    fields = ["title"]
    template_name = "task_new.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskDetail(DetailView):
    model = Task
    context_object_name = "task"
    template_name = "task_detail.html"


class TaskDelete(DeleteView):
    model = Task
    context_object_name = "task"
    template_name = "task_delete.html"
    success_url = reverse_lazy("home")


class TaskUpdate(UpdateView):
    model = Task
    context_object_name = "task"
    # fields = ["title", "is_complete"]
    template_name = "task_update.html"
    form_class = TaskUpdateForm
    success_url = reverse_lazy("home")
