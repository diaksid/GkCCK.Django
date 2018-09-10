from django import template

from ..models import Albom


register = template.Library()


@register.simple_tag
def get_albom(*args, **kwargs):
    pk = args[0] if len(args) > 0 else kwargs.get('pk')
    if pk:
        try:
            model = Albom.actives.get(pk=pk)
            return model
        except Albom.DoesNotExist:
            pass
    return None
