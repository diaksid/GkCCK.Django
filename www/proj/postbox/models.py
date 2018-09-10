from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.encoding import force_text

from proj.db.fields import StripCharField, StripTextField
from proj.db.models import FromDBModel

from .apps import PostboxConfig


class Mail(FromDBModel):
    STATE_CHOICES = (
        ('0', 'Важное',),
        ('1', 'Прочитано',),
        ('2', 'Спам',),
    )

    name = StripCharField(
        verbose_name='имя',
        max_length=128,
        db_index=True,
    )

    email = StripCharField(
        max_length=128,
        db_index=True,
    )

    phone = StripCharField(
        verbose_name='телефон',
        max_length=128,
        null=True,
        blank=True,
    )

    subject = StripCharField(
        verbose_name='тема',
        max_length=128,
        null=True,
        blank=True,
        db_index=True,
    )

    message = StripTextField(
        verbose_name='сообщение',
    )

    sent_date = models.DateTimeField(
        verbose_name='дата',
        auto_now_add=True,
        db_index=True,
    )

    state = models.CharField(
        verbose_name='тип',
        max_length=1,
        choices=STATE_CHOICES,
        null=True,
        blank=True,
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
        db_table = PostboxConfig.label
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'
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
        super(Mail, self).save(*args, **kwargs)
