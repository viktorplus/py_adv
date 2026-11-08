from rest_framework import serializers

from apps.taskmanager.models import SubTask


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = ('id', 'title', 'description', 'task', 'status', 'deadline', 'created_at')
        # read_only_fields = ('created_at',) # Alternative


class SubTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTask
        fields = ('id', 'title', 'description', 'task', 'status', 'deadline', 'created_at')
