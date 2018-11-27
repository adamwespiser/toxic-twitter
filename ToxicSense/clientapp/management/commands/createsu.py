from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            print('Creating admin user')
            User.objects.create_superuser("admin", "admin@toxicsense.com", "admin")
