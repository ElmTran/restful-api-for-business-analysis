from celery import shared_task
from .serializers import TaskCreateUpdateSerializer, ResultSerializer, AttachmentSerializer

# todo: add celery task to create a task


@shared_task
def add(task_id):
    task = TaskCreateUpdateSerializer.get_object(task_id)
    attachment = task.attachment
    result = ResultSerializer(
        data={'task': task_id, 'result': attachment.file.read()})
    result.is_valid(raise_exception=True)
    result.save()
    task.status = 'completed'
    task.save()
    return result.data
