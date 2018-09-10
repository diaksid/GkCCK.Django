from django.views.generic import ListView, DetailView
# from django.utils.translation import ugettext_lazy as _

from proj.views.generic import LangMixin

from .models import Page


class PageListView(LangMixin, ListView):

    allow_empty = False
    template_name = 'content/list.html'

    def get_queryset(self):
        return Page.navigate.filter(locale=self.lang)


class PageDetailView(LangMixin, DetailView):

    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_template_names(self):
        return ['content/%s' % (self.object.get_layout() or 'detail.html')]

    def get_queryset(self):
        return Page.publish.filter(locale=self.lang)

    def get_context_data(self, **kwargs):
        context = super(PageDetailView, self).get_context_data(**kwargs)
        data = self.kwargs.copy()
        data.pop(self.slug_url_kwarg, None)
        if data:
            context.update(data)
        return context
