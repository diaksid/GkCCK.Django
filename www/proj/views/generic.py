from django.views.generic.base import View
from django.conf import settings
from django.utils.translation import activate, get_language


class LangMixin(View):

    def get(self, request, *args, **kwargs):
        if len(settings.LANGUAGES) > 1:
            lang = get_language()
            self.lang = kwargs.get('lang', None)
            if self.lang is None:
                self.lang = lang
            if self.lang != lang:
                activate(self.lang)
        else:
            self.lang = settings.LANGUAGE_CODE
        return super(LangMixin, self).get(request, *args, **kwargs)


class LangStrictMixin(View):

    def get(self, request, *args, **kwargs):
        if len(settings.LANGUAGES) > 1:
            lang = get_language()
            self.lang = kwargs.get('lang', None)
            if self.lang is None:
                self.lang = settings.LANGUAGE_CODE
            if self.lang != lang:
                activate(self.lang)
        else:
            self.lang = settings.LANGUAGE_CODE
        return super(LangStrictMixin, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LangStrictMixin, self).get_context_data(**kwargs)
        context['LANGUAGE_URL_CODE'] = None if self.lang == settings.LANGUAGE_CODE else self.lang
        return context
