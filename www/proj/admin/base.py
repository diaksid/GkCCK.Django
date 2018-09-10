from django.contrib import admin
from django import forms
from django.conf import settings

from .filters import LocaleListFilter


class LocaleModelAdmin(admin.ModelAdmin):

    def __init__(self, *args, **kwargs):
        super(LocaleModelAdmin, self).__init__(*args, **kwargs)
        if bool(self.exclude):
            if not 'locale' in self.exclude:
                self.exclude += 'locale',
        else:
            self.exclude = 'locale',
        if len(settings.LANGUAGES) > 1:
            if not 'get_locale' in self.list_display:
                self.list_display = ('get_locale',) + self.list_display
            if not LocaleListFilter in self.list_filter:
                self.list_filter = (LocaleListFilter,) + self.list_filter

    def get_form(self, request, obj=None, **kwargs):
        if len(settings.LANGUAGES) > 1:
            class LocaleModelAdminForm(self.form):
                language = forms.ChoiceField(
                    label='Локаль',
                    choices=settings.LANGUAGES,
                    initial=obj.locale if obj else settings.LANGUAGE_CODE,
                    widget=forms.Select(attrs={
                        'class': 'col-xs-1',
                    }),
                )
            self.form = LocaleModelAdminForm
        return super(LocaleModelAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.locale = form.cleaned_data.get('language', settings.LANGUAGE_CODE)
        super(LocaleModelAdmin, self).save_model(request, obj, form, change)

    def get_locale(self, instance):
        for code, locale in settings.LANGUAGES:
            if instance.locale == code:
                return locale
        return '<%s>' % instance.locale
    get_locale.short_description = 'локаль'
    get_locale.admin_order_field = 'locale'


class SortableChangeListForm(forms.ModelForm):

    class Meta:
        widgets = {
            'index': forms.TextInput(attrs={
                'class': 'vPositiveSmallIntegerField',
                'type': 'number',
                'min': 0,
                'step': 1,
            }),
        }


class SortableModelAdmin(admin.ModelAdmin):

    def __init__(self, *args, **kwargs):
        super(SortableModelAdmin, self).__init__(*args, **kwargs)
        if not 'index' in self.list_display:
            self.list_display += 'index',
        if not 'index' in self.list_editable:
            self.list_editable += 'index',

    def get_changelist_form(self, request, **kwargs):
        return SortableChangeListForm
