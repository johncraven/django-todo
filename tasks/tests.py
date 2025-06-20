import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
from django import setup

setup()

from django.test import TestCase, SimpleTestCase  # noqa: E402
from django.urls import reverse  # noqa: E402
from django.contrib.auth import get_user_model  # noqa: E402

from tasks.models import Task  # noqa: E402


class VisitorLoginTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/auth/login/")
        self.assertEqual(response.status_code, 200)

    def test_url_exists_by_name(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_url_uses_correct_template(self):
        response = self.client.get("/auth/login/")
        self.assertEqual(response.template_name[0], "registration/login.html")


class VisitorSignupTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

    def test_url_exists_by_name(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    def test_url_uses_correct_template(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.template_name[0], "registration/signup.html")


class TodoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(
            username="testuser", password="testpass", email="testuser@email.com"
        )
        cls.task = Task.objects.create(
            title="Test Task", author=cls.user1, is_complete=False
        )

    def setUp(self):
        self.client.login(username="testuser", password="testpass")

    def test_task_create(self):
        response = self.client.post(
            reverse("task_new"),
            {"title": "New Task"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(title="New Task").exists())

    def test_task_detail(self):
        response = self.client.get(reverse("task_detail", args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.title)

    def test_task_update(self):
        response = self.client.post(
            reverse("task_update", args=[self.task.pk]),
            {"title": "Updated Task", "is_complete": True},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")

    def test_task_delete(self):
        response = self.client.post(
            reverse("task_delete", args=[self.task.pk]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
