from django.contrib import admin
from django.contrib.sites.models import Site
from django.conf import settings


class LocaleListFilter(admin.SimpleListFilter):
    title = 'локаль'
    parameter_name = 'locale'

    def lookups(self, request, model_admin):
        return settings.LANGUAGES

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(locale=value)


class SiteListFilter(admin.SimpleListFilter):
    title = 'сайт'
    parameter_name = 'site'

    def lookups(self, request, model_admin):
        return ((obj.pk, obj.name,) for obj in Site.objects.all())

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(site=value).order_by('pk')
