from .. import app_config


__version__ = '0.1.1'

config = app_config.get('postbox', {})

default_app_config = 'proj.postbox.apps.PostboxConfig'
