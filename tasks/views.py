# tasks/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from .models import Task, Comment
from .forms import TaskUpdateForm, TaskCreateForm, CommentForm


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


@login_required
def task_detail_view(request, pk: int):
    task = get_object_or_404(Task, pk=pk)
    if task.author != request.user:
        raise PermissionDenied("you don't have permission to view this task")

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.task = task
            comment.save()

    comment_form = CommentForm()  # always send back and empty form

    return render(
        request,
        template_name="task_detail.html",
        context={
            "task": task,
            "comment_form": comment_form,
            "comments": task.comments.all().order_by("-created_on"),
        },
    )


def task_create_view(request):
    if request.method == "POST":
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect("home")
    else:
        form = TaskCreateForm()
    return render(
        request=request,
        template_name="task_new.html",
        context={"form": form},
    )


class TaskCreate(CreateView, LoginRequiredMixin):
    model = Task
    form_class = TaskCreateForm
    template_name = "task_new.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskDelete(DeleteView, LoginRequiredMixin):
    model = Task
    context_object_name = "task"
    template_name = "task_delete.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user != obj.author:
            raise PermissionDenied("You don't have permission to update that task.")
        return obj


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    context_object_name = "task"
    template_name = "task_update.html"
    form_class = TaskUpdateForm
    success_url = reverse_lazy("home")

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


@require_http_methods(["PATCH"])
def task_update_complete_api(request, pk: int):
    task = get_object_or_404(Task, pk=pk)
    task.is_complete = not task.is_complete
    task.save()
    return JsonResponse(
        {
            "taskPk": task.pk,
            "isComplete": task.is_complete,
        }
    )


class CommentDelete(DeleteView):
    model = Comment

    def get_success_url(self):
        task = self.object.task
        return reverse_lazy("task_detail", kwargs={"pk": task.pk})
