from django.urls import path
from .views import (
    UserCreateAPIView,
    UserListAPIView,
    UserDetailAPIView,
)

app_name = 'users'

urlpatterns = [
    path("", UserListAPIView.as_view(), name="user-list"),
    path("register/", UserCreateAPIView.as_view(), name="user-create"),
    path("<int:id>/", UserDetailAPIView.as_view(), name="user-detail"),
]
