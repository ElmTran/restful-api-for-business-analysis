import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from models.task import Attachment
from rest_framework.test import APIClient, APITestCase
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
        response = self.client.post('/api/v1/login/', data)
        assert response.status_code == 200
        assert response.data['token']

    def test_upload(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Token {TestUser.token}'
        data = {
            'file': SimpleUploadedFile('testfile.xlsx', b'content'),
        }
        response = self.client.post('/api/v1/upload/', data=data)
        assert response.status_code == 201
        assert Attachment.objects.filter(
            original_filename='testfile.xlsx').exists()
