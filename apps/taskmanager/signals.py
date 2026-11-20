from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.taskmanager.models import Task
from apps.taskmanager.utils import send_task_status_email


@receiver(pre_save, sender=Task, dispatch_uid="task_pre_save")
def remember_old_status(sender, instance, raw, **kwargs):
    if raw or instance.pk is None:
        return
    instance._old_status = Task.objects.filter(pk=instance.pk).values_list('status', flat=True).first()


@receiver(post_save, sender=Task, dispatch_uid="task_post_save")
def notify_status_changed(sender, instance, created, raw, **kwargs):
    if raw or created:
        return
    old_status = getattr(instance, '_old_status', None)
    if old_status and old_status != instance.status:
        send_task_status_email(instance, old_status)
