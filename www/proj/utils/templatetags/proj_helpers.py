import re
from base64 import encodebytes

from django import template, get_version
from django.utils.html import format_html
from django.utils.http import urlunquote

register = template.Library()


@register.simple_tag(takes_context=True)
def render_content(context, content):
    return format_html(template.Template(content).render(context))


@register.simple_tag(takes_context=True)
def link_state_class(context, *args, **kwargs):
    href = args[0] if len(args) > 0 else kwargs.pop('href', None)
    if href == context.request.path and not context.request.GET:
        return ' active'
    elif href == context.request.path or (context.request.path.find(href) == 0 and
                                          context.request.path[len(href)] == '/'):
        return ' parent'
    else:
        return ''


@register.simple_tag(takes_context=True)
def link_state(context, *args, **kwargs):
    attr = ('%s %s' % (
               (args[1] if len(args) > 1 else kwargs.pop('class', None)) or '',
               link_state_class(context, *args, **kwargs),
            )).strip()
    return format_html(' class="%s"' % attr) if bool(attr) else ''


@register.simple_tag(takes_context=True)
def link_sign(context, *args, **kwargs):
    href = args[0] if len(args) > 0 else kwargs.pop('href', None)
    content = args[1] if len(args) > 1 else kwargs.pop('content', '')
    tag = args[2] if len(args) > 2 else kwargs.pop('tag', 'span')
    attrs = ''
    for key in kwargs:
        attrs += ' %s="%s"' % (key, kwargs[key])
    if href == context.request.path:
        html = '<%s%s>%s</%s>' % (tag, attrs, content, tag,) if bool(tag) else content
    else:
        html = '<a href="%s"%s>%s</a>' % (href, attrs, content,)
    return format_html(html)


@register.simple_tag
def get_sum(*args):
    value = args[0]
    for arg in args[1:]:
        value += arg
    return value


@register.simple_tag
def get_multiply(*args):
    value = args[0]
    for arg in args[1:]:
        value *= arg
    return value


@register.filter(is_safe=True)
def multiply(value, factor):
    return str(value * factor)


@register.simple_tag
def set_var(value):
    return value


@register.simple_tag
def set_list(*args):
    return args


@register.filter
def minify(value):
    return re.compile(r'\s+').sub(' ', value)


@register.filter
def urldecode(value):
    return urlunquote(value)


@register.filter
def base64(value):
    return encodebytes(bytes(value, 'utf-8')).decode('utf-8').strip()


@register.simple_tag
def django_version():
    return get_version()
