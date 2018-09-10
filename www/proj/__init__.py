from django.conf import settings

from .smpt import PostMultipart


__version__ = '0.1.1'

app_config = getattr(settings, 'PROJ', {})

__all__ = [
    'app_config',
    'PostMultipart',
]
