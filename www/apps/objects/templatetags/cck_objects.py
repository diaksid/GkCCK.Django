from django import template
from django.utils.translation import get_language

from ..models import Object


register = template.Library()


@register.inclusion_tag('objects/navigate.html')
def get_objects(*args, **kwargs):
    lang = get_language()
    return {
        'class': args[0] if len(args) > 0 else kwargs.get('class', None),
        'models': Object.navigate.filter(locale=lang),
        'lang': lang,
    }


@register.simple_tag
def get_object(*args, **kwargs):
    pk = args[0] if len(args) > 0 else kwargs.get('pk')
    try:
        model = Object.publish.get(pk=pk)
        return model
    except Object.DoesNotExist:
        pass
    return None


@register.simple_tag
def get_object_url(*args, **kwargs):
    pk = args[0] if len(args) > 0 else kwargs.get('pk')
    try:
        model = Object.publish.get(pk=pk)
        return model.get_absolute_url()
    except Object.DoesNotExist:
        pass
    return '#'


@register.inclusion_tag('objects/banner.html')
def get_object_banner(*args, **kwargs):
    pk = args[0] if len(args) > 0 else kwargs.get('pk')
    cover = kwargs.get('cover', None)
    try:
        object = Object.publish.get(pk=pk)
        if cover is None and object.cover:
            cover = object.cover.file
    except Object.DoesNotExist:
        pass
    return {
        'object': object,
        'width': args[1] if len(args) > 1 else kwargs.get('width'),
        'height': args[2] if len(args) > 2 else kwargs.get('height'),
        'class': kwargs.get('class', None),
        'button': kwargs.get('button', None),
        'cover': cover,
    }
