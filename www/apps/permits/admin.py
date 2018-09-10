from django.contrib import admin
from django import forms
from django.conf import settings

from proj.admin import (LocaleModelAdmin, SortableModelAdmin,
                        NoDeleteSelectedModelAdmin, PublishedModelAdmin)
from proj.gallery.admin import AlbomGenericStackedInlineAdmin

from .models import Permit


class PermitModelAdminForm(forms.ModelForm):

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
            'keywords': forms.TextInput(attrs={
                'class': 'vTextField',
            }),
            'name': forms.TextInput(attrs={
                'class': 'vLargeTextField',
            }),
            'label': forms.TextInput(attrs={
                'class': 'vTextField',
            }),
            'number': forms.TextInput(attrs={
                'class': 'vSmallTextField',
            }),
            'provider': forms.TextInput(attrs={
                'class': 'vSmallTextField',
            }),
            'note': forms.Textarea(attrs={
                'class': 'vLargeTextField autosize',
                'rows': 3,
            }),
        }


@admin.register(Permit)
class PermitModelAdmin(LocaleModelAdmin, SortableModelAdmin, NoDeleteSelectedModelAdmin, PublishedModelAdmin):

    save_as = True
    save_on_top = True

    ordering = (
        '-locale',
        'owner',
        'index',
    )

    date_hierarchy = 'issue_date'
    search_fields = [
        'title',
        'description',
        'keywords',
        'name',
        'number',
    ]
    list_display = (
        'owner',
        'index',
        'title',
        'keywords',
        'get_link',
        'get_navigate',
        'get_publish',
        'id',
    )
    list_display_links = (
        'title',
    )
    list_filter = (
        'published',
        'owner',
    )

    form = PermitModelAdminForm
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
            'owner',
            'name',
            'label',
            'number',
            'provider',
            'issue_date',
            'onset_date',
            'end_date',
            'note',
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
