from django import template

from ..forms import PostboxForm


register = template.Library()


@register.inclusion_tag('postbox/form.html')
def postbox_form(*ards, **kwards):
    prefix = ards[0] if len(ards) > 0 else kwards.get('prefix', 'postbox')
    return {
        'form': PostboxForm(prefix=prefix),
        'class': kwards.get('class', None),
    }
