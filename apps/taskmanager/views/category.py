from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.taskmanager.models import Category
from apps.taskmanager.serializers import CategoryCreateSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

    @action(detail=False, methods=['get'])
    def count_tasks(self, request):
        categories = self.get_queryset().annotate(task_count=Count('tasks'))
        data = [{'id': c.id, 'name': c.name, 'task_count': c.task_count} for c in categories]
        return Response(data)
