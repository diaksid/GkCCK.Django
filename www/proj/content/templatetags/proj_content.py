from django import template

from ..models import Page


register = template.Library()


@register.simple_tag
def content_roots():
    return ((node.get_absolute_url(), node.get_label(),) for node in Page.navigate.root_nodes())


@register.inclusion_tag('content/tree.html')
def content_tree(*args, **kwargs):
    node = args[0] if len(args) > 0 else kwargs.get('node', None)
    return {
        'node': node,
        'self': args[1] if len(args) > 1 else kwargs.get('self', None),
        'nodes': node.get_children() if node else Page.navigate.all(),
    }
