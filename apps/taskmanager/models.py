from django.db import models

def get_status_choices():
    return [
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Pending', 'Pending'),
        ('Blocked', 'Blocked'),
        ('Done', 'Done'),
    ]

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name_plural = 'categories'
        verbose_name = 'category'
        ordering = ['name']

class Task(models.Model):
    # title = models.CharField(max_length=255, unique_for_date='deadline')
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    categories = models.ManyToManyField('Category', related_name='tasks')
    status = models.CharField(max_length=20, choices=get_status_choices(), default='New')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        verbose_name_plural = 'tasks'
        verbose_name = 'task'
        ordering = ['-created_at']
        # constraints = [models.UniqueConstraint(fields=['title'], name='title_unique')]


class SubTask(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(max_length=20, choices=get_status_choices(), default='New')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        verbose_name_plural = 'subtasks'
        verbose_name = 'subtask'
        ordering = ['-created_at']
        constraints = [models.UniqueConstraint(fields=['title'], name='unique_title')]

