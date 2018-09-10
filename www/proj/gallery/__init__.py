from .. import app_config


__version__ = '0.1.1'

config = dict(
    using='default',
    root='gallery',
    thumb_size='x80',
    thumb_crop='center',
)
config.update(app_config.get('gallery', {}))


class GalleryRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == config['label']:
            return config.using
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == config['label']:
            return config.using
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == config['label'] or \
                        obj2._meta.app_label == config['label']:
            return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label == config['label']:
            return db == config.using
        return None


default_app_config = 'proj.gallery.apps.GalleryConfig'
