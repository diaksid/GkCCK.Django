from django.db import models
from django.conf import settings
from django.utils.html import strip_tags, format_html

from ..fields import StripCharField, StripTextField


class FromDBModel(models.Model):

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super(FromDBModel, cls).from_db(db, field_names, values)
        instance._loaded_values = dict(zip(field_names, values))
        return instance

    class Meta:
        abstract = True


class InfoModel(models.Model):

    title = StripCharField(
        verbose_name='заголовок',
        max_length=255,
        null=True,
        blank=True,
    )

    description = StripTextField(
        verbose_name='описание',
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return strip_tags(self.title)

    def get_description(self):
        return format_html(self.description)
    get_description.short_description = 'описание'
    get_description.admin_order_field = 'description'
    get_description.allow_tags = True


class LocaleModel(models.Model):

    locale = models.CharField(
        verbose_name='локаль',
        max_length=2,
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        abstract = True
