from django.db import models
from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.taskmanager.models import Task
from apps.taskmanager.serializers import TaskCreateSerializer, TaskDetailSerializer
from apps.taskmanager.views.mixins import BulkCreateMixin


# @api_view(['GET'])
# def hello_world(request):
#     return Response({"message": "Hello, World!"})

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


class TaskListCreateView(BulkCreateMixin, ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        day_of_week = self.request.query_params.get('day_of_week')
        if day_of_week:
            day_number = DAYS_OF_WEEK.get(day_of_week.lower())
            if day_number is None:
                raise ValidationError({"error": "Invalid day of week"})
            date_field = self.request.query_params.get('date_field', 'deadline')
            if date_field not in DATE_FIELDS:
                raise ValidationError({"error": f"date_field must be one of {DATE_FIELDS}"})
            queryset = queryset.filter(**{f'{date_field}__week_day': day_number})
        return queryset


class TaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    lookup_url_kwarg = 'task_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskDetailSerializer
        return TaskCreateSerializer


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
