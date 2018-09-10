from datetime import date

from django.conf import settings
from django.urls import reverse
from django.contrib.sitemaps import Sitemap

from .models import Article


class NewsListViewSitemap(Sitemap):

    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [('news:list', [cod[0]]) for cod in settings.LANGUAGES]

    def location(self, item):
        args = item[1] if len(settings.LANGUAGES) > 1 else None
        return reverse(item[0], args=args)

    def lastmod(self, item):
        queryset = Article.publish.filter(locale=item[1][0])
        return queryset.latest('change_date').change_date if queryset else None


class NewsDetailViewSitemap(Sitemap):

    def items(self):
        return Article.publish.all()

    def priority(self, item):
        delta = (date.today() - item.change_date.date()).days
        if delta < 30:
            return 1
        elif delta < 365:
            return 0.7
        elif item.navi:
            return 0.5
        else:
            return 0.3

    def changefreq(self, item):
        delta = (date.today() - item.change_date.date()).days
        if delta < 30:
            return 'daily'
        elif delta < 365:
            return 'weekly'
        else:
            return 'monthly'

    def lastmod(self, item):
        return item.change_date
