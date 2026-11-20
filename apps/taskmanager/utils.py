from django.conf import settings
from django.core.mail import send_mail


def send_task_status_email(task, old_status):
    if task.status == 'Done':
        subject = f'Task "{task.title}" is closed'
    else:
        subject = f'Task "{task.title}": status changed to {task.status}'
    send_mail(
        subject=subject,
        message=f'Hello, {task.owner.username}!\n\n'
                f'Task "{task.title}": {old_status} -> {task.status}\n'
                f'Deadline: {task.deadline:%d/%m/%Y %H:%M}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[task.owner.email],
    )
