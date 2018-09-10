from django.conf import settings


def yandex(request):
    context_extras = {}
    yandex = getattr(settings, 'YANDEX', None)
    if yandex:
        data = yandex.get('metrika', None)
        context_extras['yandex_metrika'] = data.get(request.site.domain, None) if type(data) is dict else data
        data = yandex.get('search', None)
        context_extras['yandex_search'] = data.get(request.site.domain, None) if type(data) is dict else data
    return context_extras


def google(request):
    data = getattr(settings, 'GOOGLE', {}).get('plus', None)
    return {
        'google_plus': data.get(request.site.domain, None) if type(data) is dict else data,
    }


def twitter(request):
    data = getattr(settings, 'TWITTER', None)
    return {
        'twitter': data.get(request.site.domain, None) if type(data) is dict else data,
    }
