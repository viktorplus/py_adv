from django.db import models

from apps.taskmanager.models.base import TimeStampedModel, get_status_choices


class Task(TimeStampedModel):
    # title = models.CharField(max_length=255, unique_for_date='deadline')
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    categories = models.ManyToManyField('Category', related_name='tasks')
    status = models.CharField(max_length=20, choices=get_status_choices(), default='New')
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        verbose_name_plural = 'tasks'
        verbose_name = 'task'
        ordering = ['-created_at']
        # constraints = [models.UniqueConstraint(fields=['title'], name='title_unique')]
