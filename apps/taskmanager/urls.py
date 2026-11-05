from django.urls import path
from apps.taskmanager.views import (
    TaskListCreateView,
    TaskDetailUpdateDeleteView,
    TaskStatsView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView
)
urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='tasks'),
    path('tasks/<int:task_id>/', TaskDetailUpdateDeleteView.as_view(), name='task-detail'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:subtask_id>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
]