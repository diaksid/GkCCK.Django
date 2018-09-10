from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.permits.sitemaps import (PermitsListViewSitemap,
                                   PermitsDetailViewSitemap)
from apps.activities.sitemaps import (ActivitiesListViewSitemap,
                                      ActivitiesDetailViewSitemap,
                                      ActivityArticlesDetailViewSitemap)
from apps.objects.sitemaps import (ObjectsListViewSitemap,
                                   ObjectsDetailViewSitemap)


class StaticViewSitemap(Sitemap):
    changefreq = 'daily'

    def items(self):
        return [
            'home',
            'about',
            'contact',
            'privacy',
        ]

    def location(self, item):
        if type(item) is str:
            return reverse(item)
        else:
            return reverse(item[0], args=item[1])

    def priority(self, item):
        return 1 if item == 'home' else 0.5

    def changefreq(self, item):
        return 'daily' if item == 'home' else 'weekly'


def sitemaps():
    return {
        'static': StaticViewSitemap,

        'permits_static': PermitsListViewSitemap,
        'permits_dynamic': PermitsDetailViewSitemap,

        'activities_static': ActivitiesListViewSitemap,
        'activities_dynamic': ActivitiesDetailViewSitemap,
        'activities_articles': ActivityArticlesDetailViewSitemap,

        'objects_static': ObjectsListViewSitemap,
        'objects_dynamic': ObjectsDetailViewSitemap,
    }
