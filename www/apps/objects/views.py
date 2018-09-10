from django.views.generic import ListView, DetailView
from django.urls import reverse

from proj.views.generic import LangMixin

from .models import Object


class ObjectListView(LangMixin, ListView):

    allow_empty = False
    paginate_by = 10
    template_name = 'objects/list.html'

    def get_queryset(self):
        return Object.navigate.filter(locale=self.lang)

    def get_context_data(self, **kwargs):
        context = super(ObjectListView, self).get_context_data(**kwargs)
        title = name = 'Объекты'
        description = 'Объекты группы компаний «ССК» осуществляющей строительный контроль, функции технического заказчика, проектирование и строительство'
        suffix = ''
        page = context['page_obj']
        if page.number > 1:
            suffix = 'стр. %d' % page.number
        if suffix:
            suffix = suffix.strip()
            name = '%s <small>%s</small>' % (title, suffix)
            title = '%s %s' % (title, suffix)
            description = '%s %s' % (description, suffix)
        context.update({
            'schema': {
                'page': 'CollectionPage',
                'creative': 'DataCatalog',
            },
            'title': title,
            'description': description,
            'name': name,
        })
        return context


class ObjectDetailView(LangMixin, DetailView):

    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'objects/detail.html'

    def get_queryset(self):
        return Object.publish.filter(locale=self.lang)

    def get_context_data(self, **kwargs):
        context = super(ObjectDetailView, self).get_context_data(**kwargs)
        context.update({
            'schema': {
                'page': 'ItemPage',
                'creative': 'Dataset',
            },
            'breadcrumbs': (
                (reverse('objects:list'), 'Объекты'),
            ),
        })
        return context
