from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination

from apps.taskmanager.models import SubTask
from apps.taskmanager.serializers import SubTaskCreateSerializer
from apps.taskmanager.views.mixins import BulkCreateMixin


class SubTaskPagination(PageNumberPagination):
    page_size = 5


class SubTaskListCreateView(BulkCreateMixin, ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    pagination_class = SubTaskPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at', '-id']

    def get_queryset(self):
        queryset = super().get_queryset()
        task_title = self.request.query_params.get('task_title')
        if task_title:
            queryset = queryset.filter(task__title__iexact=task_title)
        return queryset


class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    lookup_url_kwarg = 'subtask_id'
