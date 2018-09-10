from django.apps import AppConfig

from . import app_config


class ContentConfig(AppConfig):
    name = 'proj.content'
    label = 'proj_content'
    verbose_name = 'Контент'
