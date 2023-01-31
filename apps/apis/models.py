from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Task(models.Model):
    PROCESSING = 0, 'Processing'
    SUCCESS = 1, 'Success'
    FAILED = 2, 'Failed'
    STATUS_CHOICES = (PROCESSING, SUCCESS, FAILED,)
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks', default=1)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=PROCESSING
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tasks'
        ordering = ['-updated_at']

    @property
    def result(self):
        instance = self
        qs = Result.objects.filter(task=instance)
        if qs.exists():
            return qs.first().result
        return None

    @property
    def attachments(self):
        instance = self
        qs = Attachment.objects.filter(task=instance)
        if qs.exists():
            return qs.first().attachments
        return None


class Result(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='results')
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.result

    class Meta:
        db_table = 'results'
        ordering = ['-updated_at']


class Attachment(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments')
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='attachments', default=1
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name

    class Meta:
        db_table = 'attachments'
        ordering = ['-updated_at']
