from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(name="admin").exists():
            User.objects.create_superuser("admin", "0000000", "000000000", "00000000000", "admin@admin.com", "admin")
