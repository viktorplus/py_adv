from django.db import models
from django.utils import timezone

from apps.taskmanager.managers import SoftDeleteManager
from apps.taskmanager.models.base import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        db_table = 'task_manager_category'
        verbose_name_plural = 'categories'
        verbose_name = 'category'
        ordering = ['name']
