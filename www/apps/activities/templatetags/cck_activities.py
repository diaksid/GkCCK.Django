from django import template
from django.utils.translation import get_language

from ..models import Activity


register = template.Library()


@register.inclusion_tag('activities/links.html')
def get_activities(*args, **kwargs):
    lang = get_language()
    return {
        'class': args[0] if len(args) > 0 else kwargs.get('class', None),
        'models': Activity.navigate.filter(locale=lang),
        'lang': lang,
    }


@register.simple_tag
def get_activity(*args, **kwargs):
    pk = args[0] if len(args) > 0 else kwargs.get('pk')
    try:
        model = Activity.publish.get(pk=pk)
        return model
    except Activity.DoesNotExist:
        pass
    return None


@register.simple_tag
def get_activity_url(*args, **kwargs):
    pk = args[0] if len(args) > 0 else kwargs.get('pk')
    try:
        model = Activity.publish.get(pk=pk)
        return model.get_absolute_url()
    except Activity.DoesNotExist:
        pass
    return '#'


@register.inclusion_tag('activities/banner.html')
def get_object_banner(*args, **kwargs):
    pk = args[0] if len(args) > 0 else kwargs.get('pk')
    cover = kwargs.get('cover', None)
    try:
        object = Activity.publish.get(pk=pk)
        if cover is None:
            cover = object.cover.file
    except Activity.DoesNotExist:
        pass
    return {
        'object': object,
        'width': args[1] if len(args) > 1 else kwargs.get('width'),
        'height': args[2] if len(args) > 2 else kwargs.get('height'),
        'class': kwargs.get('class', None),
        'button': kwargs.get('button', None),
        'cover': cover,
    }


@register.inclusion_tag('activities/object.html')
def get_activity_object(*args, **kwargs):
    return {
        'object': args[0],
        'class': args[1] if len(args) > 1 else kwargs.get('class', None),
        'size': kwargs.get('size', 'x192'),
        'lazy': kwargs.get('lazy', 'canvas'),
        'width': kwargs.get('width', 256),
        'height': kwargs.get('height', 192),
        'lightbox': False,
    }
