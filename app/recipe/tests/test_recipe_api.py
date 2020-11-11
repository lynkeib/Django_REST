from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import RecipesSerializer

RECIPES_URL = reverse("recipe:recipe-list")


def sample_recipe(user, **params):
    """Create and return a sample recipe"""
    default = {
        "title": "Sample",
        "time_minute": 10,
        "price": 5
    }
    default.update(params)
    return Recipe.objects.create(user=user, **default)


class PublicRecipesApiTests(TestCase):
    """Test the publicly available recipes API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """Test the login is required for retrieving recipes"""
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipesApiTests(TestCase):
    """Test the authorized user recipes API"""

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test@test.com", "password")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Recipe.objects.create(user=self.user, name="Test1")
        Recipe.objects.create(user=self.user, name="Test2")

        res = self.client.get(RECIPES_URL)
        tags = Recipe.objects.all().order_by('-name')
        serializer = RecipesSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user("test2@test.com", "password")
        Recipe.objects.create(user=user2, name="Test1")
        tag = Recipe.objects.create(user=self.user, name="Test2")
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], tag.name)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {"name": "Test"}
        self.client.post(RECIPES_URL, payload)
        exists = Recipe.objects.filter(
            user=self.user,
            name=payload["name"]
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {"name": ""}
        res = self.client.post(RECIPES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
