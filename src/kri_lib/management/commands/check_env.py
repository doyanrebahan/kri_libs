from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Show all errors from local settings.'

    def handle(self, *args, **options):
        if not hasattr(settings, 'LOCAL_SETTINGS'):
            return
        errors = settings.LOCAL_SETTINGS.errors
        for err in errors:
            self.stderr.write(err)
