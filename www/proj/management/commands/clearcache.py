import sys

from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        verbosity = int(kwargs.get('verbosity'))
        stdout = kwargs.get('stdout', sys.stdout)

        if verbosity >= 1:
            print('cleared key_prefix = <%s>' % cache.key_prefix, end=' ... ', file=stdout)
        cache.clear()
        if verbosity >= 1:
            print('[done]', file=stdout)
