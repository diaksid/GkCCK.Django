from .. import app_config


__version__ = '0.0.1'

config = app_config.get('content', {})

default_app_config = 'proj.content.apps.ContentConfig'
