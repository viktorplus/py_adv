from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.taskmanager.models import SubTask
from apps.taskmanager.serializers import SubTaskCreateSerializer


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
