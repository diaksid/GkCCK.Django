from .. import app_config


__version__ = '0.0.1'

config = app_config.get('callback', {})

default_app_config = 'proj.callback.apps.CallbackConfig'
