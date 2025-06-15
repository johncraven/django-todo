from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.homepage_view, name="home"),
    path("task/<int:pk>/", views.TaskDetail.as_view(), name="task_detail"),
]
