from os import path

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

from proj.db.fields import StripTextField
from proj.db.models import WebLocalePageModel, PublishedModel
from proj.gallery.models import ImageGeneric
from proj.utils.helpers import slugify


class Article(WebLocalePageModel, PublishedModel):

    UPLOAD_TO = 'news'
    PATH = path.join(settings.MEDIA_ROOT, UPLOAD_TO)

    annotation = StripTextField(
        verbose_name='аннотация',
        null=True,
        blank=True,
    )

    content = StripTextField(
        verbose_name='содержание',
    )

    tags = ArrayField(
        models.CharField(max_length=32),
        size=4,
        verbose_name='ярлыки',
        null=True,
        blank=True,
    )

    source = models.URLField(
        verbose_name='источник',
        null=True,
        blank=True,
    )

    images = GenericRelation(ImageGeneric)

    class Meta(WebLocalePageModel.Meta):
        db_table = 'cck_news'
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = (
            '-locale',
            '-published_date',
            'name',
        )

    @cached_property
    def generic(self):
        return self.images.all()

    @cached_property
    def cover(self):
        if bool(self.generic):
            return self.generic[0].image
        return None

    def get_absolute_url(self):
        lang = [self.locale] if len(settings.LANGUAGES) > 1 else []
        return reverse('news:detail', args=lang + [self.slug])
    get_absolute_url.short_description = 'URI'
    get_absolute_url.admin_order_field = 'slug'

    def clean(self):
        super(Article, self).clean()
        if bool(self.tags):
            self.tags = [slugify(tag, ascii=False, space=' ') for tag in self.tags]
        try:
            model = Article.objects.get(
                locale=self.locale,
                slug=self.slug,
            )
            if model.pk != self.pk:
                raise ValidationError('Генерируется неуникальное значение URI')
        except Article.DoesNotExist:
            pass
