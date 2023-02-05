from __future__ import absolute_import, annotations
from celery import shared_task
from .serializers import TaskCreateUpdateSerializer, ResultSerializer, AttachmentSerializer
from abc import ABC, abstractmethod

# todo: add celery task


class Task(ABC):
    def __init__(self, data):
        self.data = data
        print(f"Task created: {self.data['task_type']}")

    @abstractmethod
    def preprocess(self):   # 预处理
        pass

    @abstractmethod
    def postprocess(self):  # 封装结果
        pass

    @abstractmethod
    def execute(self):
        pass

    @shared_task
    def run(self):
        self.preprocess()
        self.execute()
        self.postprocess()

    def get_result(self):
        pass


class TimeSeriesForecasting(Task):
    def __init__(self, data):
        super().__init__(data)
        self.data = data

    def preprocess(self):
        pass

    def postprocess(self):
        pass

    def execute(self):
        pass


class Classification(Task):
    def __init__(self, data):
        super().__init__(data)
        self.data = data

    def preprocess(self):
        pass

    def postprocess(self):
        pass

    def execute(self):
        pass


class Clustering(Task):
    def __init__(self, data):
        super().__init__(data)
        self.data = data

    def preprocess(self):
        pass

    def postprocess(self):
        pass

    def execute(self):
        pass


class SentimentAnalysis(Task):
    def __init__(self, data):
        super().__init__(data)
        self.data = data

    def preprocess(self):
        pass

    def postprocess(self):
        pass

    def execute(self):
        pass


class TaskCreator:
    @staticmethod
    def create_task(data):
        task_type = data['task_type']
        if task_type == 'TimeSeriesForecasting':
            return TimeSeriesForecasting(data)
        elif task_type == 'Classification':
            return Classification(data)
        elif task_type == 'Clustering':
            return Clustering(data)
        elif task_type == 'SentimentAnalysis':
            return SentimentAnalysis(data)
        else:
            raise Exception('Unknown task type')
