from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.utils import timezone

from apps.taskmanager.models import Task


class TaskStatusEmailSignalTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = get_user_model().objects.create_user(
            username='owner', email='owner@example.com', password='password123',
        )

    def setUp(self):
        self.task = Task.objects.create(
            title='Task', description='d', owner=self.owner, deadline=timezone.now() + timedelta(days=1),
        )

    def test_no_email_on_task_create(self):
        self.assertEqual(len(mail.outbox), 0)

    def test_email_sent_to_owner_on_status_change(self):
        self.task.status = 'In progress'
        self.task.save()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['owner@example.com'])
        self.assertIn('New -> In progress', mail.outbox[0].body)

    def test_closed_subject_on_done(self):
        self.task.status = 'Done'
        self.task.save()

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('is closed', mail.outbox[0].subject)

    def test_no_email_when_status_not_changed(self):
        self.task.status = 'Done'
        self.task.save()
        mail.outbox.clear()

        self.task.save()
        self.task.title = 'Renamed'
        self.task.save()

        self.assertEqual(len(mail.outbox), 0)
