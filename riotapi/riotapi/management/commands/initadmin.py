import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.filter(is_superuser=True).count() == 0:
            email = os.getenv("DJANGO_ADMIN_EMAIL")
            username = os.getenv("DJANGO_ADMIN_USERNAME")
            password = os.getenv("DJANGO_ADMIN_PASSWORD")

            if not email or not username or not password:
                print("Missing Admin User Credentials")
                return

            User.objects.create_superuser(
                email=email,
                username=username,
                password=password,
            )
        else:
            print("Admin already exists, skipping initialization")
