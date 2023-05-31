# Standard Library
import logging

# Third-Party Libraries
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView

# Project Imports
from models.task import Attachment, Result, Task
from .mixins import BaseMixin
from .pagination import TaskPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    AttachmentSerializer,
    AttachmentUploadSerializer,
    LoginSerializer,
    ResultSerializer,
    TaskCreateUpdateSerializer,
    TaskDetailSerializer,
    TaskListSerializer,
)
from .tasks import execute

# Create your views here.

logger = logging.getLogger(__name__)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            return Response(
                {
                    "token": user.auth_token.key,
                }
            )


class TaskCreateView(APIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Create a task
        serializer = self.serializer_class(data=request.data)
        attachment_id = request.data.get("attachment_id", None)
        if attachment_id is None:
            return Response(
                {"error": "Attachment ID is required."}, status=400
            )
        if serializer.is_valid(raise_exception=True):
            task = serializer.save(
                owner=self.request.user,
                attachment=get_object_or_404(Attachment, _id=attachment_id),
            )
        # 4. Run task
        task_uid = execute.delay(task._id).id
        task.uid = task_uid
        task.save()
        return Response(task_uid, status=201)


class TaskListView(ListAPIView, BaseMixin):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = TaskPagination


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self):
        return get_object_or_404(Task, id=self.kwargs["pk"])


class ResultView(APIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=self.kwargs["pk"])
        result = get_object_or_404(Result, task=task)
        serializer = self.serializer_class(result)
        return Response(serializer.data, status=200)


class AttachmentView(APIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=self.kwargs["pk"])
        attachments = task.attachments.all()
        serializer = self.serializer_class(attachments, many=True)
        return Response(serializer.data, status=200)


class UploadAttachmentView(APIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentUploadSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logger.info(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                original_filename=request.data["file"].name,
                owner=self.request.user,
                file_format=request.data["file"].name.split(".")[-1],
            )
        return Response(serializer.data, status=201)


class TestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        print(request.user)
        return Response("ok", status=201)
