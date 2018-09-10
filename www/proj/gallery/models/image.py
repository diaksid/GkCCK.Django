from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.conf import settings
from django.utils.html import strip_tags, format_html, format_html_join
from django.utils.encoding import force_text

from sorl.thumbnail import get_thumbnail, delete as delete_thumbnail

from proj.db.fields import StripCharField
from proj.db.models import InfoModel, ActiveModel

from .. import config


class ImageModel(InfoModel):

    alt = StripCharField(
        verbose_name='alt',
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    def get_alt(self):
        return force_text(self.alt if bool(self.alt) else self.get_title())


class Image(ActiveModel, ImageModel):

    file = models.ImageField(
        verbose_name='загрузить',
        width_field='width',
        height_field='height',
        null=True,
        blank=True,
    )

    width = 0
    height = 0

    path = StripCharField(
        verbose_name='путь к файлам',
        max_length=64,
        null=True,
        blank=True,
    )

    type = StripCharField(
        verbose_name='тип',
        max_length=32,
        null=True,
        blank=True,
        db_index=True,
    )

    name = StripCharField(
        verbose_name='название',
        max_length=128,
        null=True,
        db_index=True,
    )

    class Meta(ImageModel.Meta):
        ordering = (
            '-active',
            'type',
            'name',
        )

    def __str__(self):
        return strip_tags(force_text(self.name))

    def get_title(self):
        return force_text(self.title if bool(self.title) else self.name)

    def get_thumb(self, size=config['thumb_size'], crop=config['thumb_crop'], **kwargs):
        if bool(self.file):
            thumb = get_thumbnail(self.file, size, crop=crop)
            attrs = {
                'class': 'img-thumbnail hastip',
                'title': thumb.url,
                'src': thumb.url,
                'width': thumb.width,
                'height': thumb.height,
            }
            attrs.update(kwargs)
            attrs = format_html_join( ' ', '{}="{}"', ((key, attrs[key]) for key in attrs))
            return format_html('<img {}>', attrs)
        return '--'
    get_thumb.short_description = 'файл'
    get_thumb.admin_order_field = 'file'
    get_thumb.allow_tags = True

    def get_thumb_link(self, *args, **kwargs):
        if bool(self.file):
            return format_html('<a href="{}{}" target="_blank">{}</a>',
                               settings.MEDIA_URL, self.file, self.get_thumb(*args, **kwargs))
        return '--'
    get_thumb_link.short_description = 'файл'
    get_thumb_link.allow_tags = True

    def clean(self):
        self.type = self.type.lower()
        super(Image, self).clean()


@receiver(models.signals.post_delete, sender=Image)
def image_post_delete(sender, instance, **kwargs):
    if bool(instance.file):
        delete_thumbnail(instance.file, delete_file=False)


class ImageRelationModel(ImageModel):

    image = models.ForeignKey(
        Image,
        limit_choices_to={'active': True},
        related_name='+',
        verbose_name='изображение',
        on_delete=models.CASCADE,
    )

    index = models.PositiveIntegerField(
        verbose_name='индекс',
        default=0,
        db_index=True,
    )

    class Meta(ImageModel.Meta):
        abstract = True

    def __str__(self):
        return '%dx%d' % (self.image.width, self.image.height)

    @property
    def file(self):
        return self.image.file

    def get_thumb(self, *args, **kwargs):
        return self.image.get_thumb(*args, **kwargs)

    def get_title(self):
        return force_text(self.title if bool(self.title) else self.image.get_title())

    def get_description(self):
        return force_text(self.description if bool(self.description) else self.image.description)

    def get_alt(self):
        value = self.alt if bool(self.alt) else self.title
        return force_text(value if bool(value) else self.image.get_alt())


class ImageGeneric(ImageRelationModel):

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey(
        'content_type',
        'object_id',
    )

    class Meta(ImageRelationModel.Meta):
        ordering = (
            'content_type',
            'object_id',
            'index',
        )
        unique_together = (
            ('content_type', 'object_id', 'image',),
        )
