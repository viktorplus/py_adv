from rest_framework import serializers
from apps.taskmanager.models import SubTask

class SubTaskCreateSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = ('id', 'title', 'description', 'task', 'status', 'deadline', 'created_at', 'owner')
        # read_only_fields = ('created_at',) # Alternative


class SubTaskSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = SubTask
        fields = ('id', 'title', 'description', 'task', 'status', 'deadline', 'created_at', 'owner')
