from django.urls import path
from apps.taskmanager.views import task_list_create, task_detail, task_stats

urlpatterns = [
    path('tasks/', task_list_create, name='tasks'),
    path('tasks/<int:task_id>/', task_detail, name='task-detail'),
    path('tasks/stats/', task_stats, name='task-stats'),
]