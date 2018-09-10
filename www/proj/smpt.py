from smtplib import SMTP, SMTP_SSL, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr, parseaddr, make_msgid

from django.conf import settings
from django.template.loader import get_template


def _subject(subject):
    try:
        subject.encode('ascii')
    except UnicodeEncodeError:
        subject = Header(subject, 'utf-8').encode()
    return subject


def _address(address):
    if isinstance(address, str):
        address = parseaddr(address)
    name, email = address
    name = Header(name, 'utf-8').encode()
    try:
        email.encode('ascii')
    except UnicodeEncodeError:
        if '@' in email:
            box, domain = email.split('@', 1)
            box = str(Header(box, 'utf-8'))
            domain = domain.encode('idna').decode('ascii')
            email = '@'.join((box, domain,))
        else:
            email = Header(email, 'utf-8').encode()
    return formataddr((name, email,))


def _addresses(addresses):
    if isinstance(addresses, str):
        addresses = [addresses]
    return map(lambda e: _address(e), addresses)


class PostMultipart(object):

    def __init__(self, templates, data):
        self.msg = MIMEMultipart('alternative')
        self.address = _address((settings.EMAIL_SUBJECT_PREFIX, settings.DEFAULT_FROM_EMAIL,))
        if hasattr(settings, 'EMAIL_TO'):
            self.recipients = list(_addresses(settings.EMAIL_TO))
        else:
            self.recipients = [_address(settings.SERVER_EMAIL)]
        self.msg['Message-ID'] = make_msgid()
        self.msg['Sender'] = self.address
        self.msg['To'] = ', '.join(self.recipients)
        if data.get('email', None):
            self.msg['From'] = self.msg['Reply-To'] = _address((data['name'], data['email'],))
        else:
            self.msg['From'] = self.address
        self.msg['Subject'] = _subject('%s: %s' % (settings.EMAIL_SUBJECT_PREFIX, data['subject']))
        if isinstance(templates, str):
            self.msg.attach(MIMEText(get_template(templates).render(data), 'html'))
        else:
            if templates.get('plain', None):
                self.msg.attach(MIMEText(get_template(templates['plain']).render(data), 'plain'))
            if templates.get('html', None):
                self.msg.attach(MIMEText(get_template(templates['html']).render(data), 'html'))

    def send(self, debug=False):
        if settings.EMAIL_USE_SSL:
            smtp = SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
        else:
            smtp = SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        smtp.set_debuglevel(debug)
        smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        try:
            smtp.sendmail(self.address, self.recipients, self.msg.as_string())
            smtp.quit()
        except SMTPException:
            if not debug:
                raise
            return False
        return True
