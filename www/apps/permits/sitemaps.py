from datetime import date

from django.conf import settings
from django.urls import reverse
from django.contrib.sitemaps import Sitemap

from proj.utils.helpers import slugify
from .models import Permit


class PermitsListViewSitemap(Sitemap):

    priority = 0.5
    changefreq = 'daily'

    def items(self):
        owners = getattr(settings, 'PERMITS_AFFILIATES', [])
        items = []
        for cod in settings.LANGUAGES:
            items += [('permits:list', [cod[0]])]
            items += [('permits:list', [cod[0], slugify(owner)]) for owner in owners]
        return items

    def location(self, item):
        if len(settings.LANGUAGES) > 1:
            args = item[1]
        else:
            args = [item[1][1]] if len(item[1]) > 1 else None
        return reverse(item[0], args=args)

        if len(settings.LANGUAGES) == 1 and len(item[1]) == 1:
            return reverse(item[0])
        elif len(settings.LANGUAGES) == 1:
            return reverse(item[0], args=[item[1][1]])
        else:
            return reverse(item[0], args=item[1])

    def lastmod(self, item):
        kwargs = {'locale': item[1][0]}
        if len(item[1]) > 1:
            kwargs['owner'] = item[1][1]
        queryset = Permit.publish.filter(**kwargs)
        return queryset.latest('change_date').change_date if queryset else None


class PermitsDetailViewSitemap(Sitemap):

    def items(self):
        return Permit.publish.all()

    def priority(self, item):
        delta = (date.today() - item.change_date.date()).days
        if delta < 30:
            return 1
        elif delta < 365:
            return 0.7
        elif item.in_navigate:
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
