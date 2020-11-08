from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from core.models import User


class AdminSiteTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user: User = get_user_model().objects.create_superuser(
            email="admin@admin.com",
            password="password"
        )
        self.client.force_login(self.admin_user)
        self.user: User = get_user_model().objects.create_user(
            email="user@user.com",
            password="password",
            name="test"
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the usser edit page works"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
