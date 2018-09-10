from django import template
from django.utils.translation import get_language

from ..models import Article


register = template.Library()


@register.inclusion_tag('news/links.html')
def get_news(*args, **kwargs):
    lang = get_language()
    return {
        'class': args[0] if len(args) > 0 else kwargs.get('class', None),
        'models': Article.navigate.filter(locale=lang)[:5],
        'lang': lang,
    }
