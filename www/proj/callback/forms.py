from django import forms
from django.utils.translation import ugettext_lazy as _

from proj.widgets import EnclosedInput


class CallbackForm(forms.Form):

    name = forms.CharField(
        min_length=3,
        max_length=128,
        widget=EnclosedInput(attrs={
            'class': 'form-control',
            'size': '48',
            'pattern': '.{3,}',
            'title': _('не менее 3 символов'),
            'placeholder': _('Контактное лицо'),
            'required': True,
        }, prepend='icon icon-fw icon-user'),
    )

    phone = forms.RegexField(
        regex = r'^[0-9\+\-\(\)\s]{7,}$',
        min_length=7,
        max_length=128,
        widget=EnclosedInput(attrs={
            'class': 'form-control',
            'size': '48',
            'pattern': '[0-9\+\-\(\)\s]{7,}',
            'title': _('не менее 7 цифр'),
            'placeholder': _('Телефон'),
            'required': True,
        }, prepend='icon icon-fw icon-phone'),
    )

    class Meta:
        prefix = 'callback'
