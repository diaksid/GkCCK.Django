__version__ = '0.1.2'


class CommonDBRouter(object):
    def allow_migrate(self, db, app_label, model=None, **hints):
        if db == 'common':
            return app_label == 'contenttypes' or \
                   app_label == 'gallery'
        return None
