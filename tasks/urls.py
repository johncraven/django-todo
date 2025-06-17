from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.homepage_view, name="home"),
    path("task/", views.TaskCreate.as_view(), name="task_new"),
    path("task/<int:pk>/", views.TaskDetail.as_view(), name="task_detail"),
    path("task/<int:pk>/update/", views.TaskUpdate.as_view(), name="task_update"),
    path("task/<int:pk>/delete/", views.TaskDelete.as_view(), name="task_delete"),
]
