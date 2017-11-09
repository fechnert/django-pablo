from django.core.management.base import BaseCommand

from pablo.logging import logger


class Command(BaseCommand):
    help = 'Builds per-app assets'

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', 0))
        logger.loglevel = verbosity * 10
