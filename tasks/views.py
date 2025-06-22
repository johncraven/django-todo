# tasks/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms

from .models import Task, Comment
from .forms import TaskUpdateForm, TaskCreateForm


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


def task_detail_view(request, pk: int):
    task = get_object_or_404(Task, pk=pk)

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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]


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


class TaskUpdate(UpdateView, LoginRequiredMixin):
    model = Task
    context_object_name = "task"
    # fields = ["title", "is_complete"]
    template_name = "task_update.html"
    form_class = TaskUpdateForm
    success_url = reverse_lazy("home")


class CommentDelete(DeleteView):
    model = Comment

    def get_success_url(self):
        task = self.object.task
        return reverse_lazy("task_detail", kwargs={"pk": task.pk})
