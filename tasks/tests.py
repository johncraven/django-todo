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
            username="user1", password="testpass", email="user1@email.com"
        )
        cls.user2 = get_user_model().objects.create_user(
            username="user2", password="testpass", email="user2@email.com"
        )

    def setUp(self):
        self.client.login(username="user1", password="testpass")
        self.task = Task.objects.create(
            title="Test Task", author=self.user1, is_complete=False
        )

    def test_task_create_minimum_task(self):
        response = self.client.post(
            reverse("task_new"),
            {"title": "New Task"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(title="New Task").exists())

    def test_task_detail_minimum_task(self):
        response = self.client.get(reverse("task_detail", args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.title)

    def test_task_update_minimum_task(self):
        response = self.client.post(
            reverse("task_update", args=[self.task.pk]),
            {"title": "Updated Task", "is_complete": True},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")

    def test_task_delete_minimum_task(self):
        response = self.client.post(
            reverse("task_delete", args=[self.task.pk]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_create_complex_task(self):
        response = self.client.post(
            reverse("task_new"),
            {
                "title": "Complex Task",
                "description": "Step 1: complete the task...",
                "due_on": "2025-02-01",
                "priority": "1",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(title="Complex Task").exists())

    def test_task_detail_complex_task(self):
        complex_task = Task.objects.create(
            author=self.user1,
            title="Test Task 2",
            description="This is the second task in my Test Data",
            priority="1",
            due_on="2025-01-01",
        )
        response = self.client.get(reverse("task_detail", args=[complex_task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, complex_task.title)
        self.assertContains(response, complex_task.description)
        return

    def test_user1_cannot_update_user2_task(self):
        user1_task = Task.objects.create(title="my task", author=self.user1)
        self.client.login(username="user2", password="testpass")

        response = self.client.post(
            reverse("task_update", args=[user1_task.pk]),
            data={"title": "user1 sucks!"},
            follow=True,
        )
        user1_task.refresh_from_db()

        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(user1_task.title, "user1 sucks!")
        pass

    def test_user2_cannot_delete_user2_task(self):
        pass
