from datetime import date

from django.db import models

from mptt.managers import TreeManager


DB_PUBLISH_FILTER = (
    models.Q(published=True),
    models.Q(published_date__isnull=True) | models.Q(published_date__lte=date.today()),
)

DB_NAVIGATE_FILTER = (
    models.Q(published=True),
    models.Q(published_date__isnull=True) | models.Q(published_date__lte=date.today()),
    models.Q(archived=False),
)


class ActivesManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super(ActivesManager, self).get_queryset(*args, **kwargs).filter(active=True)


class ActivesMPTTManager(TreeManager):

    def get_queryset(self, *args, **kwargs):
        return super(ActivesMPTTManager, self).get_queryset(*args, **kwargs).filter(active=True)


class PublishManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super(PublishManager, self).get_queryset(*args, **kwargs).filter(*DB_PUBLISH_FILTER)


class PublishMPTTManager(TreeManager):

    def get_queryset(self, *args, **kwargs):
        return super(PublishMPTTManager, self).get_queryset(*args, **kwargs).filter(*DB_PUBLISH_FILTER)


class NavigateManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super(NavigateManager, self).get_queryset(*args, **kwargs).filter(*DB_NAVIGATE_FILTER)


class NavigateMPTTManager(TreeManager):

    def get_queryset(self, *args, **kwargs):
        return super(NavigateMPTTManager, self).get_queryset(*args, **kwargs).filter(*DB_NAVIGATE_FILTER)
