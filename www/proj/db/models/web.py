from django.db import models
from django.conf import settings
from django.utils.html import strip_tags, format_html
from django.utils.encoding import force_text

from proj.utils.helpers import slugify

from ..fields import StripCharField
from .base import LocaleModel


WEB_ROBOTS_CHOICES = (
    (None, 'ALL',),
    ('index,nofollow', 'index, no follow',),
    ('noindex,noarchive,follow', 'no index, follow',),
    ('noindex,noarchive,nofollow', 'NONE',),
)


class PageModel(models.Model):

    index = models.PositiveIntegerField(
        verbose_name='индекс',
        default=0,
        db_index=True,
    )

    robots = StripCharField(
        max_length=32,
        choices=WEB_ROBOTS_CHOICES,
        null=True,
        blank=True,
    )

    title = StripCharField(
        max_length=255,
        null=True,
        blank=True,
    )

    keywords = StripCharField(
        max_length=255,
        null=True,
        blank=True,
    )

    description = StripCharField(
        max_length=255,
        null=True,
        blank=True,
    )

    name = StripCharField(
        verbose_name='заголовок',
        max_length=255,
        null=True,
    )

    label = StripCharField(
        verbose_name='пункт меню',
        max_length=80,
        null=True,
        blank=True,
    )

    aliace = StripCharField(
        max_length=1024,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
        ordering = 'index',

    def __str__(self):
        return strip_tags(self.name)

    def get_label(self):
        return format_html(strip_tags(self.label if bool(self.label) else self.name))

    def clean(self):
        if not bool(self.title):
            self.title = force_text(strip_tags(self.name))
        self.slug = slugify(self.title)
        self.aliace = force_text(self.aliace)
        super(PageModel, self).clean()


class WebPageModel(PageModel):

    slug = StripCharField(
        verbose_name='URI',
        max_length=1024,
        null=True,
        blank=True,
        unique=True,
    )

    class Meta(PageModel.Meta):
        abstract = True


class WebLocalePageModel(LocaleModel, PageModel):

    slug = StripCharField(
        verbose_name='URI',
        max_length=1024,
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        abstract = True
        ordering = (
            '-locale',
            'index',
        )
        unique_together = (
            ('locale', 'slug',),
        )
