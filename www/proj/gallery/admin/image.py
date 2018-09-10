import os.path

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline
from django import forms
from django.conf import settings
from django.utils.html import format_html
from django.utils.encoding import force_text

from proj.admin import ActiveModelAdmin

from .. import config
from ..models import Image, ImageGeneric


class ImageModelAdminForm(forms.ModelForm):

    class Meta:
        widgets = {
            'type': forms.TextInput(attrs={
                'class': 'vSmallTextField',
            }),
            'path': forms.TextInput(attrs={
                'class': 'vSmallTextField',
            }),
            'title': forms.TextInput(attrs={
                'class': 'vLargeTextField',
            }),
            'description': forms.Textarea(attrs={
                'class': 'vLargeTextField autosize',
                'rows': 3,
            }),
        }


class ImageModelAdmin(ActiveModelAdmin):

    save_as = True
    save_on_top = True
    list_per_page = 20

    ordering = (
        '-active',
        'type',
        'name',
    )

    search_fields = (
        'name',
        'description',
        'alt',
        'file',
    )
    list_display = (
        'id',
        'type',
        'get_thumb',
        'name',
        'title',
        'get_description',
        'alt',
        'active',
    )
    list_display_links = (
        'get_thumb',
        'name',
    )
    list_filter = (
        'active',
        'type',
    )

    form = ImageModelAdminForm
    fieldsets = (
        ('Состояние и структура', {'fields': [
            'active',
            'type',
        ]}),
        ('Файл', {'fields': [
            'load',
            'get_thumb_link',
            'file',
            'path',
        ]}),
        ('Информация', {'fields': [
            'name',
            'title',
            'description',
            'alt',
        ]}),
    )
    readonly_fields = 'get_thumb_link',

    actions = [
        'make_analysis',
    ]

    def get_form(self, request, obj=None, **kwargs):
        if obj and bool(obj.path):
            path = os.path.join(settings.MEDIA_ROOT, config['root'], obj.path)
        else:
            path = os.path.join(settings.MEDIA_ROOT, config['root'])
        class CurrentImageModelAdminForm(self.form):
            load = forms.FilePathField(
                label='выбрать',
                path=path,
                recursive=True,
                match='.+\.(jpg|png|gif)$(?i)',
                required=False,
                widget=forms.Select(attrs={
                    'class': 'vSmallSelectField',
                }),
            )
        self.form = CurrentImageModelAdminForm
        return super(ImageModelAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if bool(obj.path):
            obj._meta.get_field('file').upload_to = os.path.join(config['root'], obj.path)
        else:
            obj._meta.get_field('file').upload_to = config['root']
        if bool(form.cleaned_data['load']):
            obj.file = form.cleaned_data['load'].replace('%s/' % settings.MEDIA_ROOT, '')
            obj.path = os.path.dirname(force_text(obj.file).replace('%s/' % config['root'], ''))
        super(ImageModelAdmin, self).save_model(request, obj, form, change)

    def make_analysis(self, request, queryset):
        for obj in queryset:
            if bool(obj.file):
                obj.path = os.path.dirname(force_text(obj.file).replace('%s/' % config['root'], ''))
            else:
                obj.path = None
            obj.save()
        rows = queryset.count()
        if rows == 1:
            message = 'одно изображение проанализировано'
        else:
            message = '%d изображений проанализированы' % rows
        self.message_user(request, message)
    make_analysis.short_description = 'Анализировать выбранные изображения'


class ImageInlineAdmin(object):

    extra = 0

    raw_id_fields = 'image',
    readonly_fields = (
        'image_thumb_link',
        'image_title',
        'image_description',
        'image_alt',
    )

    verbose_name = 'изображение'
    verbose_name_plural = 'изображения'

    def image_thumb_link(self, instance):
        return instance.image.get_thumb_link()
    image_thumb_link.short_description = 'файл'
    image_thumb_link.allow_tags = True

    def image_title(self, instance):
        return instance.image.get_title()
    image_title.short_description = 'заголовок'

    def image_description(self, instance):
        return format_html(instance.image.description)
    image_description.short_description = 'описание'
    image_description.allow_tags = True

    def image_alt(self, instance):
        return instance.image.get_alt()
    image_alt.short_description = 'alt'


class ImageTabularInlinelAdminForm(forms.ModelForm):

    class Meta:
        widgets = {
            'image': forms.Select(attrs={
                'class': 'vSmallSelectField',
            }),
            'title': forms.TextInput(attrs={
                'class': 'vSmallTextField',
            }),
            'description': forms.Textarea(attrs={
                'class': 'vSmallTextField autosize narrow',
                'rows': 2,
            }),
            'alt': forms.TextInput(attrs={
                'class': 'vSmallTextField',
            }),
            'index': forms.TextInput(attrs={
                'class': 'vPositiveSmallIntegerField',
                'type': 'number',
                'min': 0,
                'step': 1,
            }),
        }


class ImageTabularInlineAdmin(ImageInlineAdmin):

    form = ImageTabularInlinelAdminForm
    fields = [
        'index',
        'image',
        'image_thumb_link',
        'title',
        'description',
        'alt',
    ]


class ImageGenericTabularInlineAdmin(ImageTabularInlineAdmin, GenericTabularInline):

    model = ImageGeneric


class ImageStackedInlineAdminForm(forms.ModelForm):

    class Meta:
        widgets = {
            'image': forms.Select(attrs={
                'class': 'vSelectField',
            }),
            'description': forms.Textarea(attrs={
                'class': 'vTextField autosize',
                'rows': 3,
            }),
            'index': forms.TextInput(attrs={
                'class': 'vPositiveSmallIntegerField',
                'type': 'number',
                'min': 0,
                'step': 1,
            }),
        }


class ImageStackedInlineAdmin(ImageInlineAdmin):

    form = ImageStackedInlineAdminForm
    fields = [
        'image',
        'image_thumb_link',
        ('title', 'image_title',),
        ('description', 'image_description',),
        ('alt', 'image_alt',),
        'index',
    ]


class ImageGenericStackedInlineAdmin(ImageStackedInlineAdmin, GenericStackedInline):

    model = ImageGeneric
