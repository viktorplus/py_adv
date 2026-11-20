from django.apps import AppConfig


class TaskmanagerConfig(AppConfig):
    name = 'apps.taskmanager'

    def ready(self):
        import apps.taskmanager.signals
