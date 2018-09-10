from urllib.request import urlopen
# from django.utils.six import urlopen
from django.contrib import admin
from django.apps import apps as django_apps
from django import urls
from django.conf import settings
from django.utils.http import urlencode
from django.contrib.sitemaps import ping_google


PING_URL_YANDEX = 'http://site.yandex.ru/ping.xml'
PING_SITEMAP_URL_YANDEX = 'http://blogs.yandex.ru/pings/'
PING_URL_BING = 'http://www.bing.com/webmaster/ping.aspx'


class PingerModelAdmin(admin.ModelAdmin):

    def pinger(self, request, obj, **kwargs):
        def error(message):
            return self.message_user(request, message, 'ERROR')
        result = []

        page_url = kwargs.get('page_url', None)
        if page_url is None:
            if hasattr(obj, 'get_absolute_url'):
                page_url = obj.get_absolute_url()
            else:
                return error('<pinger> requires page url (not automatically detected)')

        if not django_apps.is_installed('django.contrib.sites'):
            return error('<pinger> requires django.contrib.sites, which is not installed')
        Site = django_apps.get_model('sites.Site')
        current_site = Site.objects.get_current()

        sitemap_url = kwargs.get('sitemap', None)
        if sitemap_url is None:
            try:
                sitemap_url = urls.reverse('django.contrib.sitemaps.views.index')
            except urls.NoReverseMatch:
                try:
                    sitemap_url = urls.reverse('django.contrib.sitemaps.views.sitemap')
                except urls.NoReverseMatch:
                    pass

        yandex = getattr(settings, 'YANDEX', {})
        if yandex.get('PING', None):
            searchs = yandex.get('SEARCH', None)
            if searchs is None:
                error('<pinger yandex> requires YANDEX SEARCH settings')
            else:
                search = searchs.get(current_site.domain, None)
                if search is None:
                    error('<pinger yandex> requires YANDEX SEARCHES settings for current (%s) domain' % current_site.domain)
                else:
                    key = search.get('key', None)
                    login = search.get('login', None)
                    search_id = search.get('searchid', None)
                    if key and login and search_id:
                        params = urlencode({
                            'key': key,
                            'login': login,
                            'search_id': search_id,
                            'urls': '%s%s' % (current_site.domain, page_url),
                        })
                        try:
                            urlopen('%s?%s' % (PING_URL_YANDEX, params))
                            result.append('Yandex')
                        except Exception:
                            error('<pinger yandex> could not open PING_URL_YANDEX')
                    else:
                        error('<pinger yandex> requires YANDEX correct settings for current (%s) domain' % current_site.domain)

        if yandex.get('PING_SITEMAP', None):
            if sitemap_url is None:
                error('<pinger yandex sitemap> requires sitemap url (not automatically detected)')
            else:
                url = 'http://%s%s' % (current_site.domain, sitemap_url)
                params = urlencode({
                    'status': 'success',
                    'url': url,
                })
                try:
                    urlopen('%s?%s' % (PING_SITEMAP_URL_YANDEX, params))
                    result.append('Yandex sitemap')
                except Exception:
                    error('<pinger yandex sitemap> could not open PING_SITEMAP_URL_YANDEX')

        google = getattr(settings, 'GOOGLE', {})
        if google.get('PING', None):
            if sitemap_url is None:
                error('<pinger google> requires sitemap url (not automatically detected)')
            else:
                try:
                    ping_google(sitemap_url)
                    result.append('Google')
                except Exception:
                    error('<pinger google> has error')

        bing = getattr(settings, 'BING', {})
        if bing.get('PING', None):
            if sitemap_url is None:
                error('<pinger bing> requires sitemap url (not automatically detected)')
            else:
                url = 'http://%s%s' % (current_site.domain, sitemap_url)
                params = urlencode({
                    'siteMap': url,
                })
                try:
                    urlopen('%s?%s' % (PING_URL_BING, params))
                    result.append('Bing')
                except Exception:
                    error('<pinger bing> could not open PING_URL_BING')

        if len(result):
            self.message_user(request, ' | '.join(result), 'INFO')
