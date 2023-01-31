from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Task, Result, Attachment

User = get_user_model()


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title',
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
            'task',
            'file',
            'updated_at',
        ]
