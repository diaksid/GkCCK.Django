import re

from django import template

register = template.Library()


@register.inclusion_tag('utils/img.html', takes_context=True)
def img(context, *args, **kwargs):
    img = context.get('img', {})
    width = kwargs.get('width', context.get('width', None)) or img.width
    height = kwargs.get('height', context.get('height', None)) or img.height
    orientation = 'portrait' if width < height else 'landscape'

    return {
        'original': kwargs.get('original', context.get('original', None)),

        'src': args[0] if len(args) > 0 else kwargs.get('src',
                                                        context.get('src',
                                                                    img.url)),
        'width': width,
        'height': height,

        'lazy': kwargs.get('lazy', context.get('lazy', None)),

        'class': kwargs.get('class', context.get('class', 'img-fluid')),
        'title': kwargs.get('title', context.get('title', '')),
        'alt': kwargs.get('alt', context.get('alt', '')),

        'lightbox': kwargs.get('lightbox', context.get('lightbox', None)),
        'orientation': orientation,

        'delay': kwargs.get('delay', context.get('delay', None)),

        'itemprop': kwargs.get('itemprop', context.get('itemprop', True)),

    }


@register.inclusion_tag('utils/canvas.html', takes_context=True)
def canvas(context, *args, **kwargs):
    img = context.get('img', {})
    width = kwargs.get('width', context.get('width', None)) or img.width
    height = kwargs.get('height', context.get('height', None)) or img.height
    orientation = 'portrait' if width < height else 'landscape'

    return {
        'original': kwargs.get('original', context.get('original', None)),

        'src': args[0] if len(args) > 0 else kwargs.get('src',
                                                        context.get('src',
                                                                    img.url)),
        'width': width,
        'height': height,

        'class': kwargs.get('class', context.get('class', 'img-fluid')),
        'title': kwargs.get('title', context.get('title', '')),

        'lightbox': kwargs.get('lightbox', context.get('lightbox', None)),
        'orientation': orientation,

        'delay': kwargs.get('delay', context.get('delay', None)),

        'itemprop': kwargs.get('itemprop', context.get('itemprop', True)),
    }


@register.inclusion_tag('utils/thumb.html', takes_context=True)
def thumb(context, *args, **kwargs):
    original = str(args[0] if len(args) > 0 else \
                   kwargs.get('original',
                              context.get('original', 'no-photo.png')))

    return {
        'original': original,

        'size': args[1] if len(args) > 1 else kwargs.get('size',
                                                         context.get('size',
                                                                     '96x96')),
        'crop': kwargs.get('crop', context.get('crop', 'noop')),
        'format': kwargs.get('format', context.get('format', 'PNG' if re.match(
            r'^.+\.png$(?i)', original) else 'JPEG')),
        'quality': kwargs.get('quality', context.get('quality', 80)),
        'progressive': kwargs.get('progressive',
                                  context.get('progressive', False)),

        'lazy': kwargs.get('lazy', context.get('lazy', None)),
        'width': kwargs.get('width', context.get('width', None)),
        'height': kwargs.get('height', context.get('height', None)),

        'class': kwargs.get('class', context.get('class', None)),
        'title': kwargs.get('title', ''),
        'alt': kwargs.get('alt', ''),

        'lightbox': kwargs.get('lightbox', context.get('lightbox', None)),

        'delay': kwargs.get('delay', None),

        'itemprop': kwargs.get('itemprop', context.get('itemprop', True)),
    }
