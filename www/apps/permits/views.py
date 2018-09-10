from django.views.generic import ListView, DetailView
from django.urls import reverse

from proj.views.generic import LangStrictMixin

from .models import Permit


class PermitMixin(LangStrictMixin):

    def get(self, request, *args, **kwargs):
        self.owner = kwargs.get('owner', None)
        return super(PermitMixin, self).get(request, *args, **kwargs)


class PermitListView(PermitMixin, ListView):

    allow_empty = False
    template_name = 'permits/list.html'

    def get_queryset(self):
        kwargs = {'locale': self.lang}
        if self.owner:
            kwargs['owner'] = self.owner
        return Permit.navigate.filter(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(PermitListView, self).get_context_data(**kwargs)
        title = 'Допуски'
        description = 'Допуски группы компаний «ССК» - свидетельства сро, лицензии, сертификаты, аттестаты'
        name = title
        owner = None
        breadcrumbs = None
        if self.owner:
            owner = Permit.OWNERS.get(self.owner, '[ %s ]' % self.owner)
            name = '%s %s' % (title, owner)
            title = '%s %s' % (title, owner)
            description = '%s %s' % (description, owner)
            breadcrumbs = (reverse('permits:list'), 'Допуски'),
        context.update({
            'schema': {
                'page': 'CollectionPage',
                'creative': 'DataCatalog',
            },
            'title': title,
            'description': description,
            'name': name,
            'owner': owner,
            'breadcrumbs': breadcrumbs,
        })
        return context


class PermitDetailView(PermitMixin, DetailView):

    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'permits/detail.html'

    def get_queryset(self):
        return Permit.publish.filter(
            locale=self.lang,
            owner=self.owner,
        )

    def get_context_data(self, **kwargs):
        context = super(PermitDetailView, self).get_context_data(**kwargs)
        owner = Permit.OWNERS.get(self.owner, '[ %s ]' % self.owner)
        context.update({
            'schema': {
                'page': 'ItemPage',
                'creative': 'Dataset',
            },
            'name': self.object.label,
            'breadcrumbs': (
                (reverse('permits:list'), 'Допуски'),
                (self.object.get_owner_url(), self.object.get_owner_name()),
            ),
        })
        return context
