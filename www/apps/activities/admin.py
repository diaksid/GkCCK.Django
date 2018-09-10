from django.contrib import admin
from django import forms
from django.conf import settings

from proj.admin import (LocaleModelAdmin, SortableModelAdmin,
                        NoDeleteSelectedModelAdmin, PublishedModelAdmin)
from proj.widgets import AutosizedTextarea

from .models import Activity, ActivityArticle


class ActivityModelAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'parent': forms.Select(attrs={
                'class': 'vTextField',
            }),
            'aliace': forms.TextInput(attrs={
                'class': 'vLargeTextField',
            }),
            'index': forms.TextInput(attrs={
                'class': 'vPositiveSmallIntegerField',
                'type': 'number',
                'min': 0,
                'step': 1,
                'size': 4,
            }),
            'title': forms.TextInput(attrs={
                'class': 'vLargeTextField',
            }),
            'description': AutosizedTextarea(attrs={
                'class': 'narrow vLargeTextField',
                'rows': 2,
            }),
            'keywords': forms.TextInput(attrs={
                'class': 'vLargeTextField',
            }),
            'name': forms.TextInput(attrs={
                'class': 'vLargeTextField',
            }),
            'label': forms.TextInput(attrs={
                'class': 'vTextField',
            }),
            'annotation': AutosizedTextarea(attrs={
                'class': 'vLargeTextField',
                'rows': 3,
            }),
            'content': AutosizedTextarea(attrs={
                'class': 'extra vLargeTextField',
                'rows': 7,
            }),
        }


@admin.register(Activity)
class ActivityModelAdmin(LocaleModelAdmin, SortableModelAdmin,
                         NoDeleteSelectedModelAdmin, PublishedModelAdmin):
    save_as = True
    save_on_top = True

    ordering = (
        '-locale',
        'index',
    )

    search_fields = [
        'title',
        'description',
        'keywords',
        'name',
    ]

    list_display = (
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
    list_filter = [
        'published',
        'archived',
    ]

    form = ActivityModelAdminForm
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
            'annotation',
            'content',
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

    def get_fieldsets(self, request, obj=None):
        if len(settings.LANGUAGES) > 1:
            fields = self.fieldsets[1][1]['fields']
            if 'language' not in fields:
                fields.insert(1, 'language')
        return self.fieldsets


@admin.register(ActivityArticle)
class ActivityArticleModelAdmin(SortableModelAdmin, NoDeleteSelectedModelAdmin,
                                PublishedModelAdmin):
    save_as = True
    save_on_top = True

    ordering = (
        'parent',
        'index',
    )

    search_fields = [
        'title',
        'description',
        'keywords',
        'name',
    ]

    list_display = (
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
        'archived',
        ('parent', admin.RelatedOnlyFieldListFilter,),
    )

    form = ActivityModelAdminForm
    fieldsets = (
        ('Публикация', {'fields': [
            'published',
            'published_date',
            'archived',
        ]}),
        ('Структура', {'fields': [
            'parent',
            'index',
            'aliace',
            'slug',
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
            'content',
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
