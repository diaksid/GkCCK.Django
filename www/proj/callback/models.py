from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.encoding import force_text

from proj.db.fields import StripCharField, StripTextField
from proj.db.models import FromDBModel

from .apps import CallbackConfig


class Order(FromDBModel):

    name = StripCharField(
        verbose_name='имя',
        max_length=128,
        db_index=True,
    )

    phone = StripCharField(
        verbose_name='телефон',
        max_length=128,
        db_index=True,
    )

    sent_date = models.DateTimeField(
        verbose_name='дата',
        auto_now_add=True,
        db_index=True,
    )

    state = models.NullBooleanField(
        verbose_name='обратный звонок',
        db_index=True,
    )

    note = StripTextField(
        verbose_name='примечание',
        null=True,
        blank=True,
    )

    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'is_staff': True},
        related_name='+',
        verbose_name='агент',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    site = models.ForeignKey(
        Site,
        related_name='+',
        verbose_name='сайт',
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = CallbackConfig.label
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = (
            'state',
            '-sent_date',
            'site',
        )

    def __str__(self):
        return force_text(self.name)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.site = Site.objects.get_current()
        super(Order, self).save(*args, **kwargs)
