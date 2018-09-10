from datetime import date

from django.urls import reverse
from django.contrib.sitemaps import Sitemap

from .models import Page


class ContentListViewSitemap(Sitemap):

    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [('content:list',)]

    def location(self, item):
        return reverse(item[0])

    def lastmod(self, item):
        queryset = Page.publish
        return queryset.latest('change_date').change_date if queryset else None


class ContentDetailViewSitemap(Sitemap):

    def items(self):
        return Page.publish.all()

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
