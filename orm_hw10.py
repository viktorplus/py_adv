import os
from datetime import date, datetime, timedelta
from idlelib import search

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from apps.taskmanager.models import SubTask, Task, Category

from django.db.models import Q, F, Count
from django.utils import timezone

############################################################
# Домашнее задание 10: Проект "Менеджер задач" — ORM запросы
############################################################
# Цель: Освоение основных операций CRUD (Create, Read, Update, Delete) на примере заданных моделей.
# Выполните запросы:
# Создание записей:

# Task:
# title: "Prepare presentation".
# description: "Prepare materials and slides for the presentation".
# status: "New".
# deadline: Today's date + 3 days.

task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status="New",
    deadline=timezone.now() + timedelta(days=3)
)

# SubTasks для "Prepare presentation":
# title: "Gather information".
# description: "Find necessary information for the presentation".
# status: "New".
# deadline: Today's date + 2 days.
# title: "Create slides".
# description: "Create presentation slides".
# status: "New".
# deadline: Today's date + 1 day.

subtask = SubTask.objects.create(
    title="Gather information",
    description="Find necessary information for the presentation",
    status="New",
    deadline=timezone.now() + timedelta(days=2),
    task=task
)

subtask2 = SubTask.objects.create(
    title="Create slides",
    description="Create presentation slides",
    status="New",
    deadline=timezone.now() + timedelta(days=1),
    task=task
)

# Чтение записей:
# Tasks со статусом "New":
task = Task.objects.filter(status="New").first()

# Вывести все задачи, у которых статус "New".
new_tasks = Task.objects.filter(status="New")
for task in new_tasks:
    print(f"Task: {task.title}, Status: {task.status}, Deadline: {task.deadline}")

# SubTasks с просроченным статусом "Done":
overdue_subtasks = SubTask.objects.filter(status="Done", updated_at__gt=F("deadline")).first()
print (overdue_subtasks)

# Вывести все подзадачи, у которых статус "Done", но срок выполнения истек.
overdue_subtasks_list = SubTask.objects.filter(status="Done", updated_at__gt=F("deadline")).all()
for subtask in overdue_subtasks_list:
    print(subtask)

# Изменение записей:
# Измените статус "Prepare presentation" на "In progress".
task_to_update = Task.objects.filter(title="Prepare presentation").first()
if task_to_update:
    task_to_update.status = "In progress"
    task_to_update.save()

# Измените срок выполнения для "Gather information" на два дня назад.
subtask_to_update = SubTask.objects.filter(title="Gather information").first()
if subtask_to_update:
    subtask_to_update.deadline = timezone.now() - timedelta(days=2)
    subtask_to_update.save()

# Измените описание для "Create slides" на "Create and format presentation slides".
subtask_to_update = SubTask.objects.filter(title="Create slides").first()
if subtask_to_update:
    subtask_to_update.description = "Create and format presentation slides"
    subtask_to_update.save()

# Удаление записей:
# Удалите задачу "Prepare presentation" и все ее подзадачи.
task_to_delete = Task.objects.filter(title="Prepare presentation").first()
if task_to_delete:
    task_to_delete.delete()