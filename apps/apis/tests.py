# Third-Party Libraries
import pandas as pd
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient, APITestCase

# Project Imports
from forecasters import ClusteringCreator, TimeSeriesForecasterCreator
from models.task import Attachment
from settings.base import TestUser

# Create your tests here.


@pytest.mark.django_db
class TestAPIView(APITestCase):
    def setup_class(self):
        self.client = APIClient()

    def test_login(self):
        data = {
            "username": TestUser.username,
            "password": TestUser.password,
        }
        response = self.client.post("/api/v1/login/", data)
        assert response.status_code == 200
        assert response.data["token"]

    def test_upload(self):
        self.client.defaults["HTTP_AUTHORIZATION"] = f"Token {TestUser.token}"
        data = {
            "file": SimpleUploadedFile("testfile.xlsx", b"content"),
        }
        response = self.client.post("/api/v1/upload/", data=data)
        assert response.status_code == 201
        assert Attachment.objects.filter(
            original_filename="testfile.xlsx"
        ).exists()


class TestModels:
    pass


class TestForecasting:
    def setup_class(self):
        self.data = pd.read_csv("attachments/time_series_test.csv")
        self.params = {
            "method": "arima",
            "features": ["Month"],
            "target": "Ridership",
            "time_format": "%m/%d/%Y",
            "rate": 0.2,
            "random_state": 0,
            "predays": 32,
        }
        self.payload = {
            "attachment_id": 1,
            "title": "Test Task",
            "category": "TimeSeriesForecasting",
            "params": self.params,
        }

    def test_time_series_forecaster(self):
        forecaster = TimeSeriesForecasterCreator(
            self.params["method"], self.data, self.params
        ).create()
        result = forecaster.forecast()
        assert result

    def test_time_series_forecaster_by_api(self):
        self.client = APIClient()
        response = self.client.post(
            "/api/v1/create", data=self.payload, format="json"
        )
        assert response.status_code == 201
        assert response.data["status"] == "PENDING"


class TestClassification:
    def setup_class(self):
        pass

    def test_classification(self):
        pass

    def test_classification_by_api(self):
        pass


class TestClustering:
    def setup_class(self):
        self.data = pd.read_csv("attachments/clustering_test.csv")
        self.params = {
            "method": "gaussian_mixture",
            "features": [
                "Balance",
                "Qual_miles",
                "cc1_miles",
                "cc2_miles",
                "cc1_miles",
                "Bonus_miles",
                "Bonus_trans",
                "Flight_miles_12mo",
                "Flight_trans_12",
                "Days_since_enroll",
                "Award?",
            ],
            "n_clusters": 3,
            "random_state": 0,
        }

    def test_clustering(self):
        forecaster = ClusteringCreator(
            self.params["method"], self.data, self.params
        ).create()
        result = forecaster.forecast()
        assert result

    def test_clustering_by_api(self):
        pass


class TestSentimentAnalysis:
    def setup_class(self):
        pass

    def test_sentiment_analysis(self):
        pass

    def test_sentiment_analysis_by_api(self):
        pass
