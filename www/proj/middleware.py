import re
import time

from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils.translation import get_language
from django.utils.encoding import force_text
from django.utils.deprecation import MiddlewareMixin

from . import app_config


class SetLanguageCookieMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if settings.USE_I18N and request.path.find('/admin') != 0 and response.status_code == 200 and 'text/html' in \
                response['Content-Type']:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, get_language())
        return response


class MinifyHTMLMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        def re_code(m):
            s = m.group(1).lstrip(u'\n\r').rstrip()
            s = s.replace(u'\n\r', '<br>').replace(u'\n', '<br>').replace(u'\r', '<br>')
            s = s.replace(u'\t', '&nbsp;' * 4).replace(u' ', '&nbsp;')
            return m.group(0).replace(m.group(1), s)

        def re_style(m):
            s = re.compile(r'\s*--\s*').sub('--', m.group(1))
            s = re.compile(r'\s*([\{\}\*\>\+\,\;])\s*').sub(r'\1', s)
            s = re.compile(r'([\[\:]) ').sub(r'\1', s)
            s = s.replace(u' ]', ']').replace(u';}', '}')
            return m.group(0).replace(m.group(1), s)

        def re_script(m):
            s = m.group(1).strip()
            if len(s):
                s = s.rstrip(u';')
                s = re.compile(r'\s*([\(\)\[\]\{\}\?\|\&\/\*\-\+\:\.\,\;\=])\s*').sub(r'\1', s)
            return m.group(0).replace(m.group(1), s)

        def re_quote(m):
            s = m.group(2).replace(u'\'', '"')
            s = re.compile(r'\s+(\S+?)="\s*([^"]+)\s*"').sub(r' \1="\2"', s)
            s = re.compile(r'(\S+?)="([^=\s]+?)"').sub(r'\1=\2', s)
            return m.group(0).replace(m.group(2), s)

        config = dict(
            minify=False,
            minify_code=False,
            minify_strict=False,
        )
        config.update(app_config.get('html', {}))

        if request.path.find('/admin') != 0 and \
                        response.status_code == 200 and 'text/html' in response['Content-Type'] and \
                        config['minify'] is True:
            value = force_text(response.content.strip())
            if config['minify_code']:
                value = re.compile(r'<pre.*?>(.+?)</pre>', re.DOTALL).sub(re_code, value)
            value = re.compile(r'\s+').sub(' ', value)
            value = re.compile(r'<(\w+)(.*?) \/?>').sub(r'<\1\2>', value)
            value = re.compile(r'> <([!\/]?)([\w+\[\]-])').sub(r'><\1\2', value)
            value = re.compile(r'<style>(.*?)</style>').sub(re_style, value)
            value = re.compile(r'<script.*?>(.*?)</script>').sub(re_script, value)
            if config['minify_strict']:
                value = re.compile(r'<([^\/\s]+)(.+?)>').sub(re_quote, value)
                value = re.compile(r'</(html|body|p|li)>').sub('', value)
            response.content = value
            response['Content-Length'] = str(len(response.content))
        return response


class MultiHostMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            request.META['LoadingStart'] = time.time()
            host = request.META['HTTP_HOST']
            host_port = host.split(':')
            if len(host_port) == 2:
                host = host_port[0]
            try:
                site = Site.objects.get(domain=host)
                settings.SITE_ID = site.id
                settings.CACHE_MIDDLEWARE_KEY_PREFIX = '%s_' % site.domain
            except Site.DoesNotExist:
                pass
            if settings.HOST_MIDDLEWARE_URLCONF_MAP.get(host, None):
                request.urlconf = settings.HOST_MIDDLEWARE_URLCONF_MAP[host]
            if hasattr(settings, 'HOST_MIDDLEWARE_EMAIL_MAP'):
                if settings.HOST_MIDDLEWARE_EMAIL_MAP.get(host, None):
                    for key in settings.HOST_MIDDLEWARE_EMAIL_MAP[host]:
                        setattr(settings, key, settings.HOST_MIDDLEWARE_EMAIL_MAP[host][key])
        except KeyError:
            pass

    def process_response(self, request, response):
        if hasattr(request.META, 'LoadingStart'):
            response['LoadingTime'] = '%.2fs' % (time.time() - int(request.META['LoadingStart']))
        if hasattr(request, 'urlconf'):
            patch_vary_headers(response, ('Host',))
        return response
