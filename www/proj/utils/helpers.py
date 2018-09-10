import re

from django.utils.encoding import force_text

from .. import app_config


def translit(value):
    from .constants import TABLE_ASCII

    value = force_text(value)

    for symb_in, symb_out in TABLE_ASCII:
        value = value.replace(symb_in, symb_out)

    return value


def restrict(value):
    from .constants import TABLE_RESTRICT

    for symb_in, symb_out in TABLE_RESTRICT:
        value = value.replace(symb_in, symb_out)

    return value


def slugify(value, **kwards):
    config = dict(
        space='-',
        lower=True,
    )
    config.update(app_config.get('slugify', {}))

    strip = kwards.get('strip', True)
    if strip:
        value = value.strip()

    strict = kwards.get('strict', True)
    if strict:
        value = restrict(value)

    ascii = kwards.get('ascii', True)
    if ascii:
        value = translit(value)

    exclude = kwards.get('exclude', None)
    if exclude:
        for symb_ex in exclude:
            value = value.replace(symb_ex, '')

    space = kwards.get('space', config['space'])
    if space:
        value = re.sub('\s+', force_text(space), value)

    lower = kwards.get('lower', config['lower'])
    if lower:
        value = value.lower()

    return value
