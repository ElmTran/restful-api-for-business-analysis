from django.urls import path
from .views import (
    TaskCreateView,
    TaskDetailView,
    TaskListView,
    ResultView,
    AttachmentView,
    UploadAttachmentView,
)

app_name = 'apis'

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("create/", TaskCreateView.as_view(), name="task-create"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("<int:pk>/result/", ResultView.as_view(), name="result-detail"),
    path(
        "<int:pk>/attachment/",
        AttachmentView.as_view(), name="attachment-detail"
    ),
    path("upload/", UploadAttachmentView.as_view(), name="upload-attachment"),
]
