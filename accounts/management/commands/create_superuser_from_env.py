import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Creates a superuser using environment variables from .env"

    def handle(self, *args, **options):
        # It is recommended to load the .env file before running Django,
        # e.g. via python-dotenv in your manage.py or settings.py.
        username = os.environ.get("SUPERUSER_USERNAME")
        email = os.environ.get("SUPERUSER_EMAIL")
        password = os.environ.get("SUPERUSER_PASSWORD")

        if not username or not email or not password:
            self.stdout.write(
                self.style.ERROR(
                    "SUPERUSER_USERNAME, SUPERUSER_EMAIL, and SUPERUSER_PASSWORD must be set in the environment."
                )
            )
            return

        User = get_user_model()
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f"Superuser '{username}' created successfully.")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Superuser '{username}' already exists.")
            )
