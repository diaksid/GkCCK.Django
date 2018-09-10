from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from django.utils.functional import cached_property

from proj.db.fields import StripCharField, StripTextField
from proj.db.models import WebLocalePageModel, PublishedModel
from proj.gallery.models import AlbomGeneric
from proj.utils.helpers import slugify


class Permit(WebLocalePageModel, PublishedModel):
    values = getattr(settings, 'PERMITS_AFFILIATES', [])
    OWNERS = {}
    OWNER_CHOICES = []
    for value in values:
        key = slugify(value)
        OWNERS[key] = value
        OWNER_CHOICES.append((key, value,))

    owner = StripCharField(
        verbose_name='владелец',
        max_length=128,
        choices=OWNER_CHOICES,
        default=OWNER_CHOICES[0][0],
        db_index=True,
    )

    number = StripCharField(
        verbose_name='номер',
        max_length=128,
        null=True,
        blank=True,
    )

    provider = StripCharField(
        verbose_name='кем выдано',
        max_length=128,
    )

    issue_date = models.DateField(
        verbose_name='дата выдачи',
        null=True,
        blank=True,
    )

    onset_date = models.DateField(
        verbose_name='начало действия',
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        verbose_name='окончание действия',
        null=True,
        blank=True,
    )

    note = StripTextField(
        verbose_name='примечания',
        null=True,
        blank=True,
    )

    alboms = GenericRelation(AlbomGeneric)


    class Meta:
        db_table = 'cck_permit'
        verbose_name = 'документ'
        verbose_name_plural = 'документы'
        ordering = (
            '-locale',
            'owner',
            'index',
        )
        unique_together = ('locale', 'owner', 'slug',),


    @cached_property
    def generic(self):
        return self.alboms.all()

    @cached_property
    def cover(self):
        if self.generic:
            return self.generic[0].cover
        return None

    def get_absolute_url(self):
        lang = [self.locale] if len(settings.LANGUAGES) > 1 else []
        return reverse('permits:detail', args=lang + [self.owner, self.slug])

    get_absolute_url.short_description = 'URI'
    get_absolute_url.admin_order_field = 'slug'

    def get_owner_name(self):
        return self.OWNERS.get(self.owner, '<%s>' % self.owner)

    def get_owner_url(self):
        lang = [self.locale] if len(settings.LANGUAGES) > 1 else []
        return reverse('permits:list', args=lang + [self.owner])

    def clean(self):
        if not bool(self.title):
            self.title = '%s %s' % (strip_tags(self.name), self.number)
        super(Permit, self).clean()

        try:
            model = Permit.objects.get(
                locale=self.locale,
                owner=self.owner,
                slug=self.slug,
            )
            if model.pk != self.pk:
                raise ValidationError('Генерируется неуникальное значение URI')
        except Permit.DoesNotExist:
            pass
