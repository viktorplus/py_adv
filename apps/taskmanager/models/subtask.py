from django.db import models

from apps.taskmanager.models.base import TimeStampedModel, get_status_choices
from apps.taskmanager.models.task import Task


class SubTask(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(max_length=20, choices=get_status_choices(), default='New')
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        verbose_name_plural = 'subtasks'
        verbose_name = 'subtask'
        ordering = ['-created_at']
        constraints = [models.UniqueConstraint(fields=['title'], name='unique_title')]
