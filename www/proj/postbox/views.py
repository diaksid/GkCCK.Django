from django.views.generic.base import RedirectView
from django.core.mail.message import EmailMultiAlternatives, sanitize_address
from django.conf import settings
from django.contrib import messages
from django.template.loader import get_template
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from .forms import PostboxForm
from .models import Mail


class PostboxRedirectView(RedirectView):
    http_method_names = ['post']

    def get(self, request, *args, **kwargs):
        if not (kwargs.get('url') or kwargs.get('pattern_name')):
            self.url = force_text(request.META.get('HTTP_REFERER'),
                                  strings_only=True, errors='replace')
            if self.url is None:
                self.pattern_name = 'home'
        self.send(request)
        return super(PostboxRedirectView, self).get(request, *args, **kwargs)

    def send(self, request):
        prefix = request.POST.get('prefix', 'postbox')
        form = PostboxForm(request.POST, prefix=prefix)
        if form.is_valid():
            data = form.cleaned_data
            del data['captcha']
            model = Mail(**data)
            model.save()
            address = sanitize_address((model.name, model.email,), 'utf-8')
            msg = EmailMultiAlternatives(
                '[%s] %s' % (settings.EMAIL_SUBJECT_PREFIX, model.subject or 'Сообщение'),
                get_template('mail/plain/contact.html').render({'model': model}),
                sanitize_address((settings.EMAIL_SUBJECT_PREFIX, settings.DEFAULT_FROM_EMAIL,), 'utf-8'),
                settings.EMAIL_TO if hasattr(settings, 'EMAIL_TO') else [settings.SERVER_EMAIL],
                headers={
                    'From': address,
                    'Sender': address,
                },
                reply_to=[address],
            )
            msg.attach_alternative(get_template('mail/html/contact.html').render({'model': model}), 'text/html')
            if msg.send() > 0:
                messages.success(request, '<b>%s!</b>' % _('Сообщение отправлено'))
            else:
                messages.error(request, '<b>%s!</b>' % _('Сообщение не отправлено'))
        else:
            if settings.DEBUG:
                for field in form.errors:
                    errors = '<b>%s</b>' % field
                    for error in form.errors[field]:
                        errors += '<br>- %s' % error
                    messages.error(request, errors)
            else:
                messages.error(request, '<b>%s!</b>' % _('Ошибка заполнения формы'))
