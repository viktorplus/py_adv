# get_status_choices is referenced by migrations/0001_initial.py as apps.taskmanager.models.get_status_choices
from apps.taskmanager.models.base import TimeStampedModel, get_status_choices
from apps.taskmanager.models.category import Category
from apps.taskmanager.models.task import Task
from apps.taskmanager.models.subtask import SubTask
