from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.encoding import force_text

from proj.db.fields import StripCharField
from proj.db.models import InfoModel, ActiveModel

from .image import Image, ImageRelationModel


class Albom(ActiveModel, InfoModel):

    public = models.BooleanField(
        verbose_name='публичный',
        default=False,
        db_index=True,
    )

    type = StripCharField(
        verbose_name='тип',
        max_length=32,
        null=True,
        blank=True,
    )

    name = StripCharField(
        verbose_name='название',
        max_length=80,
        default='',
        db_index=True,
    )

    image = models.ManyToManyField(
        Image,
        through='AlbomThrough',
        through_fields=('albom', 'image',),
        related_name='+',
        verbose_name='страницы',
    )

    class Meta(ActiveModel.Meta):
        verbose_name = 'альбом'
        verbose_name_plural = 'альбомы'

    @cached_property
    def images(self):
        return self.image.all()

    @cached_property
    def through(self):
        return self.albomthrough_set.all()

    @property
    def cover(self):
        if bool(self.through):
            return self.through[0]
        return None

    def __str__(self):
        return strip_tags(force_text(self.name))

    def get_title(self):
        return force_text(self.title if bool(self.title) else self.name)

    def get_thumb(self, *args, **kwargs):
        if bool(self.cover):
            return self.cover.get_thumb(*args, **kwargs)
        return '--'
    get_thumb.short_description = 'обложка'
    get_thumb.allow_tags = True

    def clean(self):
        self.type = self.type.lower()
        super(Albom, self).clean()


class AlbomThrough(ImageRelationModel):

    albom = models.ForeignKey(
        Albom,
        limit_choices_to={'active': True},
        verbose_name='альбом',
        on_delete=models.CASCADE,
    )

    class Meta(ImageRelationModel.Meta):
        ordering = (
            'albom',
            'index',
        )
        unique_together = (
            ('albom', 'image',),
        )


class AlbomGeneric(InfoModel):

    albom = models.ForeignKey(
        Albom,
        limit_choices_to={'active': True},
        related_name='+',
        verbose_name='альбом',
        on_delete=models.CASCADE,
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey(
        'content_type',
        'object_id',
    )

    index = models.PositiveIntegerField(
        verbose_name='индекс',
        default=0,
        db_index=True,
    )

    class Meta:
        verbose_name = 'альбом'
        verbose_name_plural = 'альбомы'
        ordering = (
            'content_type',
            'object_id',
            'index',
        )
        unique_together = (
            ('content_type', 'object_id', 'albom',),
        )

    @cached_property
    def cover(self):
        if bool(self.albom):
            return self.albom.cover
        return None

    def __str__(self):
        return '%d стр.' % self.albom.images.count()

    def get_title(self):
        return force_text(self.title if bool(self.title) else self.albom.get_title())

    def get_description(self):
        return force_text(self.description if bool(self.description) else self.albom.description)
