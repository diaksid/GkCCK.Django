from django.views.generic.base import RedirectView
from django.core.mail.message import EmailMultiAlternatives, sanitize_address
from django.conf import settings
from django.contrib import messages
from django.template.loader import get_template
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from .forms import CallbackForm
from .models import Order


class CallbackRedirectView(RedirectView):

    http_method_names = ['post']

    def get(self, request, *args, **kwargs):
        if not (kwargs.get('url') or kwargs.get('pattern_name')):
            self.url = force_text(request.META.get('HTTP_REFERER'), strings_only=True, errors='replace')
            if self.url is None:
                self.pattern_name = 'home'
        self.send(request)
        return super(CallbackRedirectView, self).get(request, *args, **kwargs)

    def send(self, request):
        prefix = request.POST.get('prefix', 'callback')
        form = CallbackForm(request.POST, prefix=prefix)
        if form.is_valid():
            model = Order(**form.cleaned_data)
            model.save()
            msg = EmailMultiAlternatives(
                '[%s] Обратный звонок' % settings.EMAIL_SUBJECT_PREFIX,
                get_template('mail/plain/callback.html').render({'model': model}),
                sanitize_address((settings.EMAIL_SUBJECT_PREFIX, settings.DEFAULT_FROM_EMAIL,), 'utf-8'),
                settings.EMAIL_TO if hasattr(settings, 'EMAIL_TO') else settings.SERVER_EMAIL,
            )
            msg.attach_alternative(get_template('mail/html/callback.html').render({'model': model}), 'text/html')
            if msg.send() > 0:
                messages.success(request,
                                 '<b>%s!</b><br>%s' %
                                 (_('Сообщение отправлено'), _('Наши менеджеры перезвонят вам в ближайшее время...')))
            else:
                messages.error(request, '<b>%s!</b>' % _('Сообщение не отправлено'))
        else:
            for field in form.errors:
                errors = '<b>%s</b>' % field
                for error in form.errors[field]:
                    errors += '<br>- %s' % error
                messages.error(request, errors)
