from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline
from django import forms
from django.utils.html import format_html

from proj.admin import SortableModelAdmin, NoDeleteSelectedModelAdmin, ActiveModelAdmin

from .image import ImageStackedInlineAdmin
from ..models import Albom, AlbomGeneric


class ImageThroughInlineAdmin(ImageStackedInlineAdmin, admin.StackedInline):

    model = Albom.image.through

    verbose_name = 'страница'
    verbose_name_plural = 'страницы'


class AlbomModelAdminForm(forms.ModelForm):

    class Meta:
        widgets = {
            'type': forms.TextInput(attrs={
                'class': 'vSmallTextField',
            }),
            'index': forms.TextInput(attrs={
                'class': 'vPositiveSmallIntegerField',
                'type': 'number',
                'min': 0,
                'step': 1,
            }),
            'title': forms.TextInput(attrs={
                'class': 'vLargeTextField',
            }),
            'description': forms.Textarea(attrs={
                'class': 'vLargeTextField autosize',
                'rows': 3,
            }),
        }


class AlbomModelAdmin(SortableModelAdmin, NoDeleteSelectedModelAdmin, ActiveModelAdmin):

    save_as = True
    save_on_top = True

    ordering = (
        '-active',
        'index',
    )

    search_fields = (
        'name',
        'description',
        'name',
    )
    list_display = (
        'index',
        'type',
        'get_thumb',
        'name',
        'title',
        'get_description',
        'public',
        'active',
        'id',
    )
    list_display_links = (
        'get_thumb',
        'name',
    )
    list_filter = (
        'active',
        'public',
        'type',
    )

    form = AlbomModelAdminForm
    fieldsets = (
        ('Состояние и структура', {'fields': [
            'active',
            'public',
            'type',
            'index',
        ]}),
        ('Информация', {'fields': [
            'name',
            'title',
            'description',
        ]}),
    )
    exclude = 'image',
    inlines = ImageThroughInlineAdmin,


class AlbomInlineAdmin(object):

    extra = 0

    raw_id_fields = 'albom',
    readonly_fields = (
        'albom_thumb',
        'albom_title',
        'albom_description',
    )

    verbose_name_plural = 'альбомы'

    def albom_thumb(self, instance):
        return instance.albom.get_thumb()
    albom_thumb.short_description = 'обложка'
    albom_thumb.allow_tags = True

    def albom_title(self, instance):
        return instance.albom.get_title()
    albom_title.short_description = 'заголовок'

    def albom_description(self, instance):
        return format_html(instance.albom.description)
    albom_description.short_description = 'описание'
    albom_description.allow_tags = True


class AlbomTabularInlineAdminForm(forms.ModelForm):

    class Meta:
        widgets = {
            'albom': forms.Select(attrs={
                'class': 'vSmallSelectField',
            }),
            'title': forms.TextInput(attrs={
                'class': 'vSmallTextField',
            }),
            'description': forms.Textarea(attrs={
                'class': 'vSmallTextField autosize narrow',
                'rows': 2,
            }),
            'index': forms.TextInput(attrs={
                'class': 'vPositiveSmallIntegerField',
                'type': 'number',
                'min': 0,
                'step': 1,
            }),
        }


class AlbomTabularInlineAdmin(AlbomInlineAdmin):

    form = AlbomTabularInlineAdminForm
    fields = [
        'index',
        'albom',
        'albom_thumb',
        'title',
        'description',
        'index',
    ]


class AlbomGenericTabularInlineAdmin(AlbomTabularInlineAdmin, GenericTabularInline):

    model = AlbomGeneric


class AlbomStackedInlineAdminForm(forms.ModelForm):

    class Meta:
        widgets = {
            'albom': forms.Select(attrs={
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


class AlbomStackedInlineAdmin(AlbomInlineAdmin):

    form = AlbomStackedInlineAdminForm
    fields = [
        'albom',
        'albom_thumb',
        ('title', 'albom_title',),
        ('description', 'albom_description',),
        'index',
    ]


class AlbomGenericStackedInlineAdmin(AlbomStackedInlineAdmin, GenericStackedInline):

    model = AlbomGeneric
