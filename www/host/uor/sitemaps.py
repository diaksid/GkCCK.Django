from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):

    changefreq = 'daily'

    def items(self):
        return [
            'home',
            'contact',
            'privacy',
            'finish',
            'install',
            'project',
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
    }
