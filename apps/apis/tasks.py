# Standard Library
import json

# Third-Party Libraries
import pandas as pd
from celery import shared_task
from serializers import ResultCreateUpdateSerializer

# Project Imports
from forecasters import TimeSeriesForecasterCreator
from models.task import Task


class TaskObj:
    def __init__(self, task):
        self.file_path = task.attachment.file.path
        self.file_format = task.attachment.format
        if self.file_format == "csv":
            self.data = pd.read_csv(self.file_path)
        elif self.file_format == "xlsx":
            self.data = pd.read_excel(self.file_path)
        else:
            raise Exception("File format not supported")
        self.params = json.loads(task.params)
        self.forecaster = None

    @shared_task
    def execute(self):
        # run forecaster
        result = self.forecaster.forecast()
        # save result to db
        serializer = ResultCreateUpdateSerializer(data=result)
        if serializer.is_valid():
            serializer.save()
            task = Task.objects.get(id=self.task.id)
            task.result = serializer.data
            task.status = Task.STATUS_CHOICES[1][0]
            task.save()
        else:
            raise Exception(serializer.errors)
        # sync task no return value

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


class Clustering(TaskObj):
    def __init__(self, data):
        super().__init__(data)


class SentimentAnalysis(TaskObj):
    def __init__(self, data):
        super().__init__(data)


class TaskCreator:
    @staticmethod
    def create_task(task):
        if task.category == "TimeSeriesForecasting":
            return TimeSeriesForecasting(task)
        elif task.category == "Classification":
            return Classification(task)
        elif task.category == "Clustering":
            return Clustering(task)
        elif task.category == "SentimentAnalysis":
            return SentimentAnalysis(task)
        else:
            raise Exception("unknown task category")
