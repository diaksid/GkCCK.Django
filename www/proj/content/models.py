from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property
from django.utils.encoding import force_text

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from proj.db.fields import StripCharField, StripTextField
from proj.db.models import WebLocalePageModel, PublishedModel
from proj.db.managers import PublishMPTTManager, NavigateMPTTManager
# from proj.gallery.models import ImageGeneric

from .apps import ContentConfig


class Page(MPTTModel, WebLocalePageModel, PublishedModel):

    parent = TreeForeignKey(
        'self',
        limit_choices_to={'cluster': True},
        verbose_name='предок',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    cluster = models.BooleanField(
        verbose_name='кластер',
        default=False,
        db_index=True,
    )

    annotation = StripTextField(
        verbose_name='аннотация',
        null=True,
        blank=True,
    )

    content = StripTextField(
        verbose_name='содержание',
    )

    source = models.URLField(
        verbose_name='источник',
        max_length=255,
        null=True,
        blank=True,
    )

    layout = StripCharField(
        verbose_name='шаблон',
        max_length=255,
        null=True,
        blank=True,
    )

    publish = PublishMPTTManager()
    navigate = NavigateMPTTManager()

    class MPTTMeta:
        tree_id_attr = 'mptt_tree'
        level_attr = 'mptt_level'
        left_attr = 'mptt_left'
        right_attr = 'mptt_right'
        order_insertion_by = ['index']

    class Meta(WebLocalePageModel.Meta):
        db_table = ContentConfig.label
        verbose_name = 'страница'
        verbose_name_plural = 'страницы'
        ordering = (
            'mptt_tree',
            'mptt_left',
        )

    def get_absolute_url(self):
        return reverse('content:detail', args=[self.slug])
    get_absolute_url.short_description = 'URL'
    get_absolute_url.admin_order_field = 'slug'

    def get_layout(self):
        if bool(self.layout):
            return self.layout
        elif bool(self.parent):
            return self.parent.get_layout()
        return None
    get_layout.short_description = 'шаблон'

    def inherit(self):
        super(Page, self).clean()
        self.slug = '%s/%s' % (self.parent.slug, self.slug)
        self.save()

    def clean(self):
        super(Page, self).clean()
        if not self.is_leaf_node():
            self.cluster = True
        if bool(self.parent):
            if self.parent.pk == self.pk:
                raise ValidationError('Элемент не может быть потомком самому себе')
            self.slug = '%s/%s' % (self.parent.slug, self.slug)
        try:
            model = Page.objects.get(slug=self.slug)
            if model.pk != self.pk:
                raise ValidationError('Генерируется неуникальное значение URI')
        except Page.DoesNotExist:
            pass

    def save(self, *args, **kwargs):
        commit = adding = self._state.adding
        if not adding:
            for field in self._loaded_values:
                if self._loaded_values[field] != getattr(self, field):
                    commit = True
                    break
        if commit:
            super(Page, self).save(*args, **kwargs)
            if not adding and self._loaded_values['slug'] != self.slug:
                for model in self.get_children():
                    model.inherit()
            Page._tree_manager.rebuild()
