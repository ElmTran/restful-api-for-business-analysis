# Third-Party Libraries
import pandas as pd
from celery import shared_task

# Project Imports
from apps.apis.serializers import ResultCreateUpdateSerializer
from forecasters import (
    ClassifierCreator,
    ClusteringCreator,
    SentimentAnalyzerCreator,
    TimeSeriesForecasterCreator,
)
from models.task import Task


class TaskObj:
    def __init__(self, task):
        self.file_path = task.attachment.file.path
        self.file_format = task.attachment.file_format
        if self.file_format == "csv":
            self.data = pd.read_csv(self.file_path)
        elif self.file_format == "xlsx":
            self.data = pd.read_excel(self.file_path)
        else:
            raise Exception("File format not supported")
        self.params = task.params
        self.forecaster = None

    def get_result(self):
        pass


class TimeSeriesForecasting(TaskObj):
    def __init__(self, data):
        super().__init__(data)
        self.forecaster = TimeSeriesForecasterCreator(
            self.params["method"], self.data, self.params
        ).create()


class Classification(TaskObj):
    def __init__(self, data):
        super().__init__(data)
        self.forecaster = ClassifierCreator(
            self.params["method"], self.data, self.params
        ).create()


class Clustering(TaskObj):
    def __init__(self, data):
        super().__init__(data)
        self.forecaster = ClusteringCreator(
            self.params["method"], self.data, self.params
        ).create()


class SentimentAnalysis(TaskObj):
    def __init__(self, data):
        super().__init__(data)
        if self.params["method"] == "text":
            self.data = self.params["text"]
        self.forecaster = SentimentAnalyzerCreator(
            self.params["method"], self.data, self.params
        ).create()


class TaskCreator:
    task_dict = {
        0: TimeSeriesForecasting,
        1: Classification,
        2: Clustering,
        3: SentimentAnalysis,
    }

    @staticmethod
    def create_task(task):
        task_obj = TaskCreator.task_dict.get(task.category)
        if task_obj:
            return task_obj(task)
        else:
            raise Exception("Task category not supported")


@shared_task
def execute(task_id):
    task = Task.objects.get(_id=task_id)
    task_obj = TaskCreator.create_task(task)
    result = task_obj.forecaster.forecast()
    data = {"result": result}
    serializer = ResultCreateUpdateSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        task = Task.objects.get(_id=task._id)
        task.result = serializer.instance
        task.status = Task.STATUS_CHOICES[1][0]
        task.save()
    else:
        raise Exception(serializer.errors)
