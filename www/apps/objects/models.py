from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

from proj.db.fields import StripCharField, StripTextField
from proj.db.models import WebLocalePageModel, PublishedModel
from proj.gallery.models import AlbomGeneric

from apps.activities.models import Activity


class Object(WebLocalePageModel, PublishedModel):
    actual = models.BooleanField(
        verbose_name='в работе',
        default=False,
        db_index=True,
    )

    address = StripCharField(
        verbose_name='адрес',
        max_length=255,
    )

    longitude = models.FloatField(
        verbose_name='долгота',
        default=0,
        blank=True,
    )

    latitude = models.FloatField(
        verbose_name='широта',
        default=0,
        blank=True,
    )

    zoom = models.PositiveSmallIntegerField(
        verbose_name='зум',
        null=True,
        blank=True,
    )

    customer = StripCharField(
        verbose_name='заказчик',
        max_length=128,
    )

    developer = StripCharField(
        verbose_name='застройщик',
        max_length=128,
        null=True,
        blank=True,
    )

    start_date = models.DateField(
        verbose_name='начало работ',
        null=True,
        blank=True,
    )

    finish_date = models.DateField(
        verbose_name='окончание работ',
        null=True,
        blank=True,
    )

    note = StripTextField(
        verbose_name='примечания',
        null=True,
        blank=True,
    )

    activity = models.ManyToManyField(
        Activity,
        limit_choices_to={'published': True},
        db_table='cck_object_activity',
        verbose_name='деятельность',
        blank=True,
    )

    alboms = GenericRelation(AlbomGeneric)


    class Meta:
        db_table = 'cck_object'
        verbose_name = 'объект'
        verbose_name_plural = 'объекты'
        ordering = (
            '-locale',
            '-actual',
            'index',
        )
        unique_together = ('locale', 'slug',),


    @cached_property
    def activities(self):
        return self.activity.all()

    @cached_property
    def generic(self):
        return self.alboms.all()

    @cached_property
    def cover(self):
        if bool(self.generic):
            return self.generic[0].albom.cover
        return None

    def get_absolute_url(self):
        lang = [self.locale] if len(settings.LANGUAGES) > 1 else []
        return reverse('objects:detail', args=lang + [self.slug])

    get_absolute_url.short_description = 'URI'
    get_absolute_url.admin_order_field = 'slug'

    def clean(self):
        super(Object, self).clean()
        self.longitude = abs(self.longitude) if bool(self.longitude) else 0
        self.latitude = abs(self.latitude) if bool(self.latitude) else 0
        self.zoom = abs(self.zoom) if bool(self.zoom) else None
        try:
            model = Object.objects.get(
                locale=self.locale,
                slug=self.slug,
            )
            if model.pk != self.pk:
                raise ValidationError('Генерируется неуникальное значение URI')
        except Object.DoesNotExist:
            pass
