from django.contrib import admin
from django import forms
from django.conf import settings

from mptt.admin import MPTTModelAdmin

from proj.admin import (LocaleModelAdmin, SortableModelAdmin,
                        NoDeleteSelectedModelAdmin, PublishedModelAdmin)
from proj.widgets import AutosizedTextarea

from .models import Page


class PageModelAdminForm(forms.ModelForm):

    class Meta:
        widgets = {
            'parent': forms.Select(attrs={
                'class': 'vLargeSelectField',
            }),
            'index': forms.TextInput(attrs={
                'class': 'vPositiveSmallIntegerField',
                'type': 'number',
                'min': 0,
                'step': 1,
            }),
            'aliace': forms.TextInput(attrs={
                'class': 'vLargeTextField',
            }),
            'robots': forms.Select(attrs={
                'class': 'vSmallTextField',
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
            'source': forms.TextInput(attrs={
                'class': 'vTextField',
            }),
            'layout': forms.TextInput(attrs={
                'class': 'vSmallTextField',
            }),
        }


@admin.register(Page)
class PageModelAdmin(LocaleModelAdmin, SortableModelAdmin, NoDeleteSelectedModelAdmin, PublishedModelAdmin, MPTTModelAdmin):

    mptt_level_indent = 40
    mptt_indent_field = 'index'
    save_as = True
    list_per_page = 20

#    change_list_template = 'admin/content/page/change_list.html'

    ordering = (
        'mptt_tree',
        'mptt_left',
    )

    search_fields = [
        'name',
        'title',
        'description',
        'keywords',
        'slug',
    ]
    list_display = (
        'id',
        'index',
        'title',
        'description',
        'keywords',
        'get_link',
        'get_layout',
        'get_navigate',
        'get_publish',
    )
    list_display_links = (
        'title',
        'description',
        'keywords',
    )
    list_filter = (
        'published',
        'archived',
    )

    form = PageModelAdminForm
    fieldsets = (
        ('Публикация', {'fields': (
            'published',
            'published_date',
            'archived',
        )}),
        ('Структура', {'fields': [
            'parent',
            'index',
            'cluster',
            'aliace',
            'slug',
        ]}),
        ('SEO', {'fields': (
            'title',
            'description',
            'keywords',
            'robots',
        )}),
        ('Контент', {'fields': [
            'name',
            'label',
            'annotation',
            'content',
            'source',
        ]}),
        ('Журнал', {'fields': (
            'create_date',
            'create_by',
            'change_date',
            'change_by',
        ), 'classes': (
            'collapse',
        )}),
    )
#    raw_id_fields = 'parent',
    readonly_fields = [
        'slug',
        'create_date',
        'create_by',
        'change_date',
        'change_by',
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj and not obj.is_leaf_node():
            return self.readonly_fields + ['cluster']
        return self.readonly_fields

    def get_fieldsets(self, request, obj=None):
        if len(settings.LANGUAGES) > 1:
            fields = self.fieldsets[1][1]['fields']
            if 'language' not in fields:
                fields.insert(1, 'language')
        fields = self.fieldsets[3][1]['fields']
        if obj and (obj.cluster or obj.parent is None):
            if 'layout' not in fields:
                fields.append('layout')
        elif 'layout' in fields:
            fields.remove('layout')
        return self.fieldsets
