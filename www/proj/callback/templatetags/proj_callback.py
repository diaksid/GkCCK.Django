from django import template

from ..forms import CallbackForm


register = template.Library()


@register.inclusion_tag('callback/form.html')
def callback_form(*ards, **kwards):
    prefix = ards[0] if len(ards) > 0 else kwards.get('prefix', 'callback')
    return {
        'form': CallbackForm(prefix=prefix),
        'class': kwards.get('class', None),
    }
