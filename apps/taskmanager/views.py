from django.db import models
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.taskmanager.models import Task
from apps.taskmanager.serializers import TaskCreateSerializer


# @api_view(['GET'])
# def hello_world(request):
#     return Response({"message": "Hello, World!"})

@api_view(['GET', 'POST'])
def task_list_create(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskCreateSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = TaskCreateSerializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'GET':
        serializer = TaskCreateSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method in ['PUT', 'PATCH']:
        serializer = TaskCreateSerializer(task, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def task_stats(request):
    by_status = Task.objects.values('status').annotate(total=models.Count('id'))
    count_all_tasks = Task.objects.count()
    deadline_passed_tasks = Task.objects.filter(deadline__lt=timezone.now()).count()
    result = {
        "count_all_tasks": count_all_tasks,
        "by_status": by_status,
        "deadline_passed_tasks": deadline_passed_tasks
    }
    return Response(result, status=status.HTTP_200_OK)
