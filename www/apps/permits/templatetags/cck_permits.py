from django import template
from django.utils.translation import get_language, ugettext_lazy as _

from ..models import Permit


register = template.Library()


@register.inclusion_tag('permits/links.html')
def get_permits(*args, **kwargs):
    lang = get_language()
    return {
        'class': args[0] if len(args) > 0 else kwargs.get('class', None),
        'items': [{'owner': item[0], 'label': _(item[1])} for item in Permit.OWNER_CHOICES],
        'lang': lang,
    }


@register.simple_tag
def get_permit(*args, **kwargs):
    pk = args[0] if len(args) > 0 else kwargs.get('pk')
    try:
        model = Permit.publish.get(pk=pk)
        return model
    except Permit.DoesNotExist:
        pass
    return None


@register.simple_tag
def get_permit_url(*args, **kwargs):
    pk = args[0] if len(args) > 0 else kwargs.get('pk')
    try:
        model = Permit.publish.get(pk=pk)
        return model.get_absolute_url()
    except Permit.DoesNotExist:
        pass
    return '#'
