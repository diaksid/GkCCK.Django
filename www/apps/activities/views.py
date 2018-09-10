from django.views.generic import ListView, DetailView
from django.http import Http404
from django.urls import reverse
from django.conf import settings

from proj.views.generic import LangStrictMixin

from .models import Activity, ActivityArticle


class ActivityListView(LangStrictMixin, ListView):

    allow_empty = False
    template_name = 'activities/list.html'

    def get_queryset(self):
        return Activity.navigate.filter(locale=self.lang)

    def get_context_data(self, **kwargs):
        context = super(ActivityListView, self).get_context_data(**kwargs)
        context.update({
            'schema': {
                'page': 'CollectionPage',
                'creative': 'DataCatalog',
            },
            'title': 'Направления деятельности',
            'description': 'Направления деятельности группы компаний «ССК» - строительный контроль,проектирование и строительство',
            'keywords': 'строительный контроль, проектирование, строительство',
        })
        return context


class ActivityDetailView(LangStrictMixin, DetailView):

    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'activities/detail.html'

    def get_queryset(self):
        return Activity.publish.filter(locale=self.lang)

    def get_context_data(self, **kwargs):
        context = super(ActivityDetailView, self).get_context_data(**kwargs)
        context.update({
            'schema': {
                'page': 'ItemPage',
                'creative': 'Dataset',
            },
            'breadcrumbs': (
                (reverse('activities:list'), 'Деятельность'),
            ),
        })
        return context


class ActivityArticleView(LangStrictMixin, DetailView):

    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'activities/article.html'

    def get(self, request, *args, **kwargs):
        try:
            model = Activity.publish.get(
                locale=kwargs['lang'] if len(settings.LANGUAGES) > 1 else settings.LANGUAGE_CODE,
                slug=kwargs['activity'],
            )
            self.activity = model
            return super(ActivityArticleView, self).get(request, *args, **kwargs)
        except Activity.DoesNotExist:
            raise Http404()

    def get_queryset(self):
        return ActivityArticle.publish.filter(parent=self.activity.pk)

    def get_context_data(self, **kwargs):
        context = super(ActivityArticleView, self).get_context_data(**kwargs)
        context.update({
            'breadcrumbs': (
                (reverse('activities:list'), 'Деятельность'),
                (self.activity.get_absolute_url(), self.activity.get_label()),
            ),
        })
        return context
