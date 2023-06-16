# Third-Party Libraries
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import models

# Create your models here.

User = get_user_model()


class Attachment(models.Model):
    _id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to="attachments")
    original_filename = models.CharField(max_length=200)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="attachments", default=1
    )
    file_format = models.CharField(max_length=20, default="csv")
    size = property(lambda self: self.file.size)
    url = property(lambda self: self.file.url)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name

    @classmethod
    def create(cls, file_name, content):
        file_csv = ContentFile(content, file_name)
        attachment = cls(
            file=file_csv,
            original_filename=file_name,
            owner=User.objects.get(username="worker"),
        )
        attachment.save()
        return attachment

    class Meta:
        db_table = "attachments"
        ordering = ["-updated_at"]


class Result(models.Model):
    _id = models.AutoField(primary_key=True)
    result = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(
        upload_to="results/", null=True, blank=True, default=None
    )

    def __str__(self):
        return self.result

    class Meta:
        db_table = "results"
        ordering = ["-updated_at"]


class Task(models.Model):
    PROCESSING = 0, "Processing"
    SUCCESS = 1, "Success"
    FAILED = 2, "Failed"
    STATUS_CHOICES = (
        PROCESSING,
        SUCCESS,
        FAILED,
    )
    CATEGORY_CHOICES = (
        (0, "TimeSeriesForecasting"),
        (1, "Classification"),
        (2, "Clustering"),
        (3, "SentimentAnalysis"),
    )
    _id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True, default=None)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks", default=1
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=PROCESSING[0]
    )
    category = models.IntegerField(choices=CATEGORY_CHOICES, default=0)
    params = models.JSONField(default=dict)
    uid = models.CharField(max_length=200, null=True, blank=True, default=None)
    attachment = models.ForeignKey(
        Attachment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
    result = models.ForeignKey(
        Result,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "tasks"
        ordering = ["-updated_at"]
