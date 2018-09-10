from django.views.generic import ListView, DetailView
from django.utils.translation import activate, ugettext_lazy as _

from proj.views.generic import LangStrictMixin

from .models import Article


class ArticleListView(LangStrictMixin, ListView):

    allow_empty = False
    paginate_by = 10
    template_name = 'news/list.html'

    def get(self, request, *args, **kwargs):
        self.year = self.kwargs.get('year', None)
        self.month = self.kwargs.get('month', None)
        self.day = self.kwargs.get('day', None)
        self.tag = request.GET.get('tag', None)
        return super(ArticleListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        kwargs = {'locale': self.lang}
        if self.year:
            kwargs['published_date__year'] = self.year
            if self.month:
                kwargs['published_date__month'] = self.month
                if self.day:
                    kwargs['published_date__day'] = self.day
        if self.tag:
            kwargs['tags__contains'] = [self.tag]
        return Article.navigate.filter(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        title = _('Новости')
        if self.lang == 'ru':
            description = 'Новости группы компаний «ССК»'
        else:
            description = 'News of the group of companies «MSQ»'
        suffix = ''
        if self.year:
            suffix = self.year
            if self.month:
                suffix = '%s/%s' % (self.month, suffix)
                if self.day:
                    suffix = '%s/%s' % (self.day, suffix)
        if self.tag:
            suffix = '%s [%s]' % (suffix, self.tag)
        page = context['page_obj']
        if page.number > 1:
            suffix = '%s %s %s' % (suffix, _('стр.'), page.number)
        if suffix:
            suffix = suffix.strip()
            name = '%s <small>%s</small>' % (title, suffix)
            title = '%s %s' % (title, suffix)
            description = '%s %s' % (description, suffix)
        else:
            name = title
        context.update({
            'schema': {
                'page': 'CollectionPage',
                'creative': 'DataCatalog',
            },
            'title': title,
            'caption': _('ГК «ССК»'),
            'description': description,
            'name': name,
        })
        return context


class ArticleDetailView(LangStrictMixin, DetailView):

    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'news/detail.html'

    def get_queryset(self):
        return Article.publish.filter(locale=self.lang)

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context.update({
            'schema': {
                'page': 'ItemPage',
                'creative': 'NewsArticle',
                'content': 'articleBody',
            },
        })
        return context
