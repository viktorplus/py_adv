from rest_framework import serializers
from apps.taskmanager.models import Task

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'deadline')

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        return task

