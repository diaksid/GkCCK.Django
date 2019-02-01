from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.admin.templatetags.admin_static import static


def _make_attrs(attrs, defaults=None, classes=None):
    result = defaults.copy() if defaults else {}
    if attrs:
        result.update(attrs)
    if classes:
        result['class'] = ' '.join((classes, result.get('class', '')))
    return result


class EnclosedInput(forms.TextInput):
    def __init__(self, attrs=None, prepend=None, append=None):
        self.prepend = prepend
        self.append = append
        super(EnclosedInput, self).__init__(attrs=attrs)

    def enclose(self, value):
        if not value.startswith('<'):
            value = format_html('<span class="{}"></span>', value)
        return format_html('<span class="input-group-addon">{}</span>', value)

    def render(self, name, value, attrs=None, renderer=None):
        output = super(EnclosedInput, self).render(name, value, attrs)
        if self.prepend:
            addon = self.enclose(self.prepend)
            output = format_html('{}{}', addon, output)
        if self.append:
            addon = self.enclose(self.append)
            output = format_html('{}{}', output, addon)
        return format_html('<div class="input-group">{}</div>', output)


class AutosizedTextarea(forms.Textarea):
    def __init__(self, attrs=None, options=None):
        self.options = options
        new_attrs = _make_attrs(attrs, {'rows': 3}, 'autosize')
        super(AutosizedTextarea, self).__init__(new_attrs)

    @property
    def media(self):
        return forms.Media(js=[static('admin/js/jquery.autosize.min.js')])

    def render(self, name, value, attrs=None, renderer=None):
        output = super(AutosizedTextarea, self).render(name, value, attrs)
        script = format_html(
            "<script>(jQuery||django.jQuery)('#id_{}').autosize()</script>",
            name)
        return mark_safe(''.join((output, script)))
