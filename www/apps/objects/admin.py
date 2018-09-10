from django.contrib import admin
from django import forms
from django.conf import settings
from django.utils.html import strip_tags, format_html

from proj.admin import (LocaleModelAdmin, SortableModelAdmin,
                        NoDeleteSelectedModelAdmin, PublishedModelAdmin)
from proj.gallery.admin import AlbomGenericStackedInlineAdmin

from .models import Object


class ObjectModelAdminForm(forms.ModelForm):

    class Meta:
        widgets = {
            'aliace': forms.TextInput(attrs={
                'class': 'vLargeTextField',
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
                'class': 'vLargeTextField autosize narrow',
                'rows': 2,
            }),
            'name': forms.TextInput(attrs={
                'class': 'vLargeTextField',
            }),
            'zoom': forms.TextInput(attrs={
                'class': 'vPositiveSmallIntegerField',
                'type': 'number',
                'min': 8,
                'max': 20,
                'step': 1,
            }),
            'note': forms.Textarea(attrs={
                'class': 'vLargeTextField autosize',
                'rows': 3,
            }),
        }


@admin.register(Object)
class ObjectModelAdmin(LocaleModelAdmin, SortableModelAdmin, NoDeleteSelectedModelAdmin, PublishedModelAdmin):

    save_as = True
    save_on_top = True

    ordering = (
        '-locale',
        '-actual',
        'index',
    )

    search_fields = [
        'name',
        'title',
        'description',
        'description',
    ]
    list_display = (
        'index',
        'actual',
        'get_thumb',
        'get_name',
        'customer',
        'get_link',
        'get_navigate',
        'get_publish',
        'id',
    )
    list_display_links = (
        'get_thumb',
        'get_name',
    )
    # list_editable = 'actual',
    list_filter = (
        'published',
        'archived',
        'actual',
        'customer',
    )

    form = ObjectModelAdminForm
    fieldsets = (
        ('Публикация', {'fields': [
            'published',
            'published_date',
            'archived',
        ]}),
        ('Структура', {'fields': [
            'aliace',
            'slug',
            'index',
        ]}),
        ('SEO', {'fields': [
            'title',
            'description',
            'keywords',
            'robots',
        ]}),
        ('Контент', {'fields': [
            'name',
            'label',
            'address',
            ('longitude', 'latitude', 'zoom',),
            'customer',
            'developer',
            'start_date',
            'finish_date',
            'note',
            'actual',
            'activity',
        ]}),
        ('История', {'fields': [
            'create_date',
            'create_by',
            'change_date',
            'change_by',
        ], 'classes': [
            'collapse',
        ]}),
    )
    filter_horizontal = 'activity',
    readonly_fields = (
        'slug',
        'create_date',
        'create_by',
        'change_date',
        'change_by',
    )
    exclude = 'alboms',
    inlines = AlbomGenericStackedInlineAdmin,

    def get_fieldsets(self, request, obj=None):
        if len(settings.LANGUAGES) > 1:
            fields = self.fieldsets[1][1]['fields']
            if 'language' not in fields:
                fields.insert(1, 'language')
        return self.fieldsets

    def get_thumb(self, instance):
        if bool(instance.cover):
            return instance.cover.get_thumb()
        return '--'
    get_thumb.short_description = 'обложка'
    get_thumb.allow_tags = True

    def get_name(self, instance):
        return format_html(instance.name)
    get_name.short_description = 'название'
    get_name.allow_tags = True
    get_name.admin_order_field = 'name'
