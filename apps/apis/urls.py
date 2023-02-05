from django.urls import path
from .views import (
    LoginView,
    TaskCreateView,
    TaskDetailView,
    TaskListView,
    ResultView,
    AttachmentView,
    UploadAttachmentView,
    TestView,
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
    path('test/', TestView.as_view(), name='test'),
    path("upload/", UploadAttachmentView.as_view(), name="upload-attachment"),
    path("login/", LoginView.as_view(), name="login"),
]
