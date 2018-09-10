from django import forms
from django.utils.translation import ugettext_lazy as _

from captcha.fields import ReCaptchaField

from proj.widgets import EnclosedInput


class PostboxForm(forms.Form):

    captcha = ReCaptchaField()

    name = forms.CharField(
        min_length=3,
        max_length=128,
        widget=EnclosedInput(attrs={
            'class': 'form-control form-control-required',
            'size': '48',
            'pattern': '.{3,}',
            'title': _('не менее 3 символов'),
            'placeholder': _('Контактное лицо'),
            'required': True,
        }, prepend='icon icon-fw icon-user'),
    )

    email = forms.EmailField(
        min_length=7,
        max_length=128,
        widget=EnclosedInput(attrs={
            'class': 'form-control form-control-required',
            'size': '48',
            'type': 'email',
            'placeholder': _('Электронный адрес'),
            'title': _('не менее 7 символов'),
            'required': True,
        }, prepend='icon icon-fw icon-envelope'),
    )

    phone = forms.RegexField(
        regex = r'^[0-9\+\-\(\)\s]{7,}$',
        min_length=7,
        max_length=128,
        required=False,
        widget=EnclosedInput(attrs={
            'class': 'form-control',
            'size': '48',
            'pattern': '[0-9\+\-\(\)\s]{7,}',
            'title': _('не менее 7 цифр'),
            'placeholder': _('Телефон'),
        }, prepend='icon icon-fw icon-phone'),
    )

    subject = forms.CharField(
        max_length=128,
        required=False,
        widget=EnclosedInput(attrs={
            'class': 'form-control',
            'size': '48',
            'placeholder': _('Тема'),
        }, prepend='icon icon-fw icon-tag'),
    )

    message = forms.CharField(
        min_length=3,
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-required autosize',
            'rows': 7,
            'placeholder': _('Сообщение'),
            'data-redactor': True,
            'required': True,
        }),
    )

    class Meta:
        prefix = 'postbox'
