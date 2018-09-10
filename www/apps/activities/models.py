from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

from proj.db.fields import StripTextField
from proj.db.models import WebPageModel, WebLocalePageModel, PublishedModel


class Activity(WebLocalePageModel, PublishedModel):
    annotation = StripTextField(
        verbose_name='аннотация',
        null=True,
        blank=True,
    )

    content = StripTextField(
        verbose_name='содержание',
    )


    class Meta(WebLocalePageModel.Meta):
        db_table = 'cck_activity'
        verbose_name = 'деятельность'
        verbose_name_plural = 'деятельности'


    @cached_property
    def articles(self):
        return self.activityarticle_set.all()

    @cached_property
    def targets(self):
        return self.object_set.all()

    def targets_actual(self):
        return self.targets.filter(actual=True)

    def targets_unactual(self):
        return self.targets.filter(actual=False)

    def get_absolute_url(self):
        lang = [self.locale] if len(settings.LANGUAGES) > 1 else []
        return reverse('activities:detail', args=lang + [self.slug])

    get_absolute_url.short_description = 'URI'
    get_absolute_url.admin_order_field = 'slug'

    def clean(self):
        super(Activity, self).clean()
        try:
            model = Activity.objects.get(
                locale=self.locale,
                slug=self.slug,
            )
            if model.pk != self.pk:
                raise ValidationError('Генерируется неуникальное значение URI')
        except Activity.DoesNotExist:
            pass


class ActivityArticle(WebPageModel, PublishedModel):
    parent = models.ForeignKey(
        Activity,
        verbose_name='предок',
        null=True,
        on_delete=models.CASCADE,
    )

    content = StripTextField(
        verbose_name='содержание',
    )


    class Meta:
        db_table = 'cck_activity_article'
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = (
            'parent',
            'index',
        )
        unique_together = ('parent', 'slug',),


    def get_absolute_url(self):
        lang = [self.parent.locale] if len(settings.LANGUAGES) > 1 else []
        return reverse('activities:content', args=lang + [self.parent.slug, self.slug])

    get_absolute_url.short_description = 'URI'
    get_absolute_url.admin_order_field = 'slug'

    def clean(self):
        super(ActivityArticle, self).clean()
        if self.aliace.find('//') == -1:
            try:
                model = ActivityArticle.objects.get(
                    parent=self.parent,
                    slug=self.slug,
                )
                if model.pk != self.pk:
                    raise ValidationError('Генерируется неуникальное значение URI')
            except ActivityArticle.DoesNotExist:
                pass
