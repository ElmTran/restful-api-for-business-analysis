from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Task(models.Model):
    PROCESSING = 0, 'Processing'
    SUCCESS = 1, 'Success'
    FAILED = 2, 'Failed'
    STATUS_CHOICES = (PROCESSING, SUCCESS, FAILED,)
    CATEGORY_CHOICES = (
        (0, 'TimeSeriesForecasting'),
        (1, 'Classification'),
        (2, 'Clustering'),
        (3, 'SentimentAnalysis'),
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True, default=None)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks', default=1)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=PROCESSING
    )
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default=0
    )
    attachment = models.ForeignKey(
        'Attachment', on_delete=models.CASCADE, null=True, blank=True, default=None)
    params = models.JSONField(default=dict)
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
    file = models.FileField(upload_to='attachments')
    original_filename = models.CharField(max_length=200)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='attachments', default=1
    )
    format = models.CharField(max_length=20, default='csv')
    size = property(lambda self: self.file.size)
    url = property(lambda self: self.file.url)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name

    class Meta:
        db_table = 'attachments'
        ordering = ['-updated_at']
