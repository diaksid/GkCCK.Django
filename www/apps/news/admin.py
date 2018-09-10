from django.contrib import admin
from django import forms
from django.conf import settings

from proj.admin import (LocaleModelAdmin,
                        NoDeleteSelectedModelAdmin, PublishedModelAdmin)
from proj.gallery.admin import ImageGenericStackedInlineAdmin

from .models import Article


class ArticleModelAdminForm(forms.ModelForm):

    class Meta:
        widgets = {
            'aliace': forms.TextInput(attrs={
                'class': 'vLargeTextField',
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
            'annotation': forms.Textarea(attrs={
                'class': 'vLargeTextField autosize',
                'rows': 3,
            }),
            'content': forms.Textarea(attrs={
                'class': 'vLargeTextField autosize push',
                'rows': 7,
            }),
            'tags': forms.TextInput(attrs={
                'class': 'vSmallTextField',
            }),
        }


@admin.register(Article)
class ArticleAdmin(LocaleModelAdmin, NoDeleteSelectedModelAdmin, PublishedModelAdmin):

    save_as = True
    save_on_top = True

    ordering = (
        '-locale',
        '-published_date',
        'name',
    )

    date_hierarchy = 'published_date'
    search_fields = [
        'title',
        'description',
        'keywords',
        'name',
    ]
    list_display = (
        'get_thumb',
        'published_date',
        'title',
        'keywords',
        'get_link',
        'get_navigate',
        'get_publish',
        'id',
    )
    list_display_links = (
        'get_thumb',
        'title',
        'keywords',
    )
    list_filter = (
        'published',
        'archived',
    )

    form = ArticleModelAdminForm
    fieldsets = (
        ('Публикация', {'fields': [
            ('published', 'published_date',),
            'archived',
        ]}),
        ('Структура', {'fields': [
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
            'annotation',
            'content',
            'tags',
            'source',
        ]}),
        ('Журнал', {'fields': [
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
    exclude = 'images',
    inlines = ImageGenericStackedInlineAdmin,

    def get_thumb(self, instance):
        if bool(instance.cover):
            return instance.cover.get_thumb()
        return '--'
    get_thumb.short_description = 'обложка'
    get_thumb.allow_tags = True

    def get_fieldsets(self, request, obj=None):
        if len(settings.LANGUAGES) > 1:
            fields = self.fieldsets[1][1]['fields']
            if 'language' not in fields:
                fields.insert(1, 'language')
        return self.fieldsets
