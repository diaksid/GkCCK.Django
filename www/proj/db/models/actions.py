from datetime import date

from django.db import models
from django.conf import settings
from django.utils.html import strip_tags, format_html

from ..fields import StripCharField
from ..managers import ActivesManager, PublishManager, NavigateManager
from .base import FromDBModel


class ActiveModel(models.Model):

    active = models.BooleanField(
        verbose_name='активно',
        default=False,
        db_index=True,
    )

    index = models.PositiveIntegerField(
        verbose_name='индекс',
        default=0,
        db_index=True,
    )

    objects = models.Manager()
    actives = ActivesManager()

    class Meta:
        abstract = True
        ordering = (
            '-active',
            'index',
        )


class PublishedModel(FromDBModel):

    published = models.BooleanField(
        verbose_name='в публикации',
        default=False,
        db_index=True,
    )

    published_date = models.DateField(
        verbose_name='старт',
        null=True,
        blank=True,
        db_index=True,
    )

    archived = models.BooleanField(
        verbose_name='в архиве',
        default=False,
        db_index=True,
    )

    create_date = models.DateTimeField(
        verbose_name='создано',
        auto_now_add=True,
    )

    create_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'is_staff': True},
        related_name='+',
        verbose_name='автор',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    change_date = models.DateTimeField(
        verbose_name='изменено',
        auto_now=True,
    )

    change_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'is_staff': True},
        related_name='+',
        verbose_name='редактор',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    objects = models.Manager()
    publish = PublishManager()
    navigate = NavigateManager()

    class Meta:
        abstract = True

    def get_publish(self):
        return bool(self.published) and (not bool(self.published_date) or self.published_date <= date.today())
    get_publish.short_description = 'публикация'
    get_publish.boolean = True
    in_publish = property(get_publish)

    def get_navigate(self):
        return not bool(self.archived) if self.in_publish else None
    get_navigate.short_description = 'навигация'
    get_navigate.boolean = True
    in_navigate = property(get_navigate)

    def get_link(self):
        url = self.get_absolute_url()
        return format_html('<a target="_blank" href="%s" title="%s">%s</a>' % (url, url, url))
    get_link.short_description = 'URL'
    get_link.admin_order_field = 'slug'
    get_link.allow_tags = True
