from django.contrib import admin

from .utils import PingerModelAdmin


class NoDeleteSelectedModelAdmin(admin.ModelAdmin):

    def get_actions(self, request):
        actions = super(NoDeleteSelectedModelAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class ActiveModelAdmin(admin.ModelAdmin):

    verbose_name = verbose_name_plural = None

    def __init__(self, *args, **kwargs):
        super(ActiveModelAdmin, self).__init__(*args, **kwargs)
        self.verbose_name = self.model._meta.verbose_name
        self.verbose_name_plural = self.model._meta.verbose_name_plural
        self.actions += [
            'make_active',
            'make_inactive',
        ]

    def make_active(self, request, queryset):
        rows = queryset.update(active=True)
        if rows == 1:
            message = '%s активирован(а)' % self.verbose_name
        else:
            message = '%d %s активированы' % (rows, self.verbose_name_plural)
        self.message_user(request, message)
    make_active.short_description = 'Активировать выбранные %(verbose_name_plural)s'

    def make_inactive(self, request, queryset):
        rows = queryset.update(active=False)
        if rows == 1:
            message = '%s деактивирован' % self.verbose_name
        else:
            message = '%d %s деактивированы' % (rows, self.verbose_name_plural)
        self.message_user(request, message)
    make_inactive.short_description = 'Деактивировать выбранные %(verbose_name_plural)s'


class PublishedModelAdmin(PingerModelAdmin):

    verbose_name = verbose_name_plural = None

    def __init__(self, *args, **kwargs):
        super(PublishedModelAdmin, self).__init__(*args, **kwargs)
        self.verbose_name = self.model._meta.verbose_name
        self.verbose_name_plural = self.model._meta.verbose_name_plural
        self.actions += [
            'make_published',
            'make_unpublished',
            'make_archived',
            'make_unarchived',
        ]

    def save_model(self, request, obj, form, change):
        commit = not change
        if not change:
            obj.create_by = obj.change_by = request.user
        else:
            for field in obj._loaded_values:
                if obj._loaded_values[field] != getattr(obj, field):
                    obj.change_by = request.user
                    commit = True
                    break
        if commit:
            super(PublishedModelAdmin, self).save_model(request, obj, form, change)
            if obj.in_publish:
                self.pinger(request, obj)

    def make_published(self, request, queryset):
        rows = queryset.update(published=True)
        if rows == 1:
            message = '%s опубликован(а)' % self.verbose_name
        else:
            message = '%d %s опубликованы' % (rows, self.verbose_name_plural)
        self.message_user(request, message)
    make_published.short_description = 'Опубликовать выбранные %(verbose_name_plural)s'

    def make_unpublished(self, request, queryset):
        rows = queryset.update(published=False)
        if rows == 1:
            message = '%s снят(а) с публикации' % self.verbose_name
        else:
            message = '%d %s сняты с публикации' % (rows, self.verbose_name_plural)
        self.message_user(request, message)
    make_unpublished.short_description = 'Снять с публикации выбранные %(verbose_name_plural)s'

    def make_archived(self, request, queryset):
        rows = queryset.update(archived=True)
        if rows == 1:
            message = '%s архивирован(а)' % self.verbose_name
        else:
            message = '%d %s архивированы' % (rows, self.verbose_name_plural)
        self.message_user(request, message)
    make_archived.short_description = 'Архивировать выбранные %(verbose_name_plural)s'

    def make_unarchived(self, request, queryset):
        rows = queryset.update(archived=False)
        if rows == 1:
            message = '%s разархивирован(а)' % self.verbose_name
        else:
            message = '%d %s разархивированы' % (rows, self.verbose_name_plural)
        self.message_user(request, message)
    make_unarchived.short_description = 'Разархивировать выбранные %(verbose_name_plural)s'
