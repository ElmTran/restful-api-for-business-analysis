from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from models.task import Task, Result, Attachment
from settings.base import env

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username and password:
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                return user
            else:
                raise serializers.ValidationError(
                    'Unable to login with provided credentials.')
        else:
            raise serializers.ValidationError(
                'Must include "username" and "password"')


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title',
            'category',
            'params',
        ]

    def validate_title(self, value):
        qs = Task.objects.filter(title__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "This title has already been used.")
        if len(value) < 3:
            raise serializers.ValidationError(
                "The title must be at least 3 characters long.")
        if len(value) > 100:
            raise serializers.ValidationError(
                "The title must be no more than 200 characters long.")
        return value


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'owner',
            'status',
            'updated_at',
        ]


class TaskDetailSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    result = serializers.SerializerMethodField(read_only=True)
    attachments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'owner',
            'result',
            'attachments',
            'status',
            'updated_at',
        ]


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = [
            'id',
            'task',
            'result',
            'updated_at',
        ]


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = [
            'id',
            'uid',
            'url',
            'file',
            'format',
            'size',
            'updated_at',
            'created_at',
        ]


class AttachmentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = [
            'file',
        ]

    def validate_file(self, value):
        if value.size > env.int('FILE_UPLOAD_MAX_MEMORY_SIZE'):
            raise serializers.ValidationError("The file is too large.")

        file_suffix = value.name.split('.')[-1]
        if file_suffix not in env.list('FILE_UPLOAD_ALLOWED_SUFFIX'):
            raise serializers.ValidationError("The file type is not allowed.")

        return value
