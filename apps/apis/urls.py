# Third-Party Libraries
from django.urls import path

from .views import (
    LoginView,
    ResultFileView,
    ResultView,
    TaskCreateView,
    TaskDetailView,
    TaskListView,
    TestView,
    UploadAttachmentView,
)

app_name = "apis"

urlpatterns = [
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("create/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("result/<str:pk>/", ResultView.as_view(), name="result-detail"),
    path("download/<str:pk>/", ResultFileView.as_view(), name="result-file"),
    path("test/", TestView.as_view(), name="test"),
    path("upload/", UploadAttachmentView.as_view(), name="upload-attachment"),
    path("login/", LoginView.as_view(), name="login"),
]

# todo: download result
