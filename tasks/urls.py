from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.homepage_view, name="home"),
    path("task/", views.TaskCreate.as_view(), name="task_new"),
    path("task/<int:pk>/", views.task_detail_view, name="task_detail"),
    path("task/<int:pk>/update/", views.TaskUpdate.as_view(), name="task_update"),
    path("task/<int:pk>/delete/", views.TaskDelete.as_view(), name="task_delete"),
    path(
        "comment/<int:pk>/delete/", views.CommentDelete.as_view(), name="comment_delete"
    ),
    path(
        "api/task/<int:pk>/update_complete",
        views.task_update_complete_api,
        name="api_task_update_complete",
    ),
]
