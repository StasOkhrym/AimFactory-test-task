from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from api.models import Genre, Person, Movie


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin.user", password="admin1234",
        )
        self.client.force_login(self.admin_user)


