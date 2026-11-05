from django.db import models
from django.utils import timezone

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.taskmanager.models import Task, SubTask
from apps.taskmanager.serializers import TaskCreateSerializer, SubTaskCreateSerializer, TaskDetailSerializer


# @api_view(['GET'])
# def hello_world(request):
#     return Response({"message": "Hello, World!"})
"""Задание 1:
Написать, или обновить, если уже есть, эндпоинт на получение списка всех задач по дню недели.
Если никакой параметр запроса не передавался - по умолчанию выводить все записи.
Если был передан день недели (например вторник) - выводить список задач только на этот день недели.

чтобы клиент сам выбирал, по какому полю фильтровать, deadline или created_at."""

# Django week_day lookup: Sunday=1 ... Saturday=7
DAYS_OF_WEEK = {
    'sunday': 1,
    'monday': 2,
    'tuesday': 3,
    'wednesday': 4,
    'thursday': 5,
    'friday': 6,
    'saturday': 7,
}
DATE_FIELDS = ('deadline', 'created_at')


class TaskListCreateView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        day_of_week = request.query_params.get('day_of_week')
        if day_of_week:
            day_number = DAYS_OF_WEEK.get(day_of_week.lower())
            if day_number is None:
                return Response({"error": "Invalid day of week"}, status=status.HTTP_400_BAD_REQUEST)
            date_field = request.query_params.get('date_field', 'deadline')
            if date_field not in DATE_FIELDS:
                return Response({"error": f"date_field must be one of {DATE_FIELDS}"},
                                status=status.HTTP_400_BAD_REQUEST)
            tasks = tasks.filter(**{f'{date_field}__week_day': day_number})
        serializer = TaskCreateSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailUpdateDeleteView(APIView):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, task_id):
        return self._update(request, task_id, partial=False)

    def patch(self, request, task_id):
        return self._update(request, task_id, partial=True)

    def delete(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _update(self, request, task_id, partial):
        task = get_object_or_404(Task, id=task_id)
        serializer = TaskCreateSerializer(task, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskStatsView(APIView):
    def get(self, request):
        by_status = Task.objects.values('status').annotate(total=models.Count('id'))
        count_all_tasks = Task.objects.count()
        deadline_passed_tasks = Task.objects.filter(deadline__lt=timezone.now()).count()
        result = {
            "count_all_tasks": count_all_tasks,
            "by_status": by_status,
            "deadline_passed_tasks": deadline_passed_tasks
        }
        return Response(result, status=status.HTTP_200_OK)


class SubTaskListCreateView(APIView, PageNumberPagination):
    page_size = 5

    def get(self, request):
        filters = {}
        task_title = request.query_params.get('task_title')
        subtask_status = request.query_params.get('status')
        if task_title:
            filters['task__title__iexact'] = task_title
        if subtask_status:
            filters['status__iexact'] = subtask_status
        subtasks = SubTask.objects.filter(**filters).order_by('-created_at', '-id')
        page = self.paginate_queryset(subtasks, request, view=self)
        serializer = SubTaskCreateSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, subtask_id):
        return get_object_or_404(SubTask, id=subtask_id)

    def get(self, request, subtask_id):
        subtask = self.get_object(subtask_id)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, subtask_id):
        subtask = self.get_object(subtask_id)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, subtask_id):
        subtask = self.get_object(subtask_id)
        serializer = SubTaskCreateSerializer(subtask, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subtask_id):
        subtask = self.get_object(subtask_id)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)