from django.views.defaults import (bad_request, permission_denied,
                                   page_not_found, server_error)
from django.views.generic import View
from django.views.generic.base import TemplateView

from braces import views

from .json import partners


def http400(request, exception):
    return bad_request(request, exception, 'proj/error/400.html')


def http403(request, exception):
    return permission_denied(request, exception, 'proj/error/403.html')


def http404(request, exception):
    return page_not_found(request, exception, 'proj/error/404.html')


def http500(request):
    return server_error(request, 'proj/error/500.html')


class RobotsView(TemplateView):
    content_type = 'text/plain'
    template_name = 'proj/robots.disallow.html'


class PartnersJSONAjaxView(views.JSONResponseMixin, views.AjaxResponseMixin,
                           View):
    def get_ajax(self, request, *args, **kwargs):
        return self.render_json_response(partners)


class HomePageView(TemplateView):
    template_name = 'www/content/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context.update(dict(
            title='Группа компаний «ССК»',
            name='Современные Стандарты Качества',
            description="""Группа компаний «ССК» предлагает услуги по
                           выполнению функций технического заказчика,
                           строительному контролю, проектированию и
                           строительству""",
            keywords="""функции технического заказчика,
                        строительный контроль,
                        проектирование,
                        строительство""",
            breadcrumbs=False,
            caption=False,
        ))
        return context


class AboutPageView(TemplateView):
    template_name = 'www/content/about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutPageView, self).get_context_data(**kwargs)
        context.update(dict(
            schema={
                'page': 'AboutPage',
            },
            title='О группе компаний «ССК»',
            description="""О группе компаний «ССК» осуществляющей
                           функции технического заказчика,
                           строительный контроль, проектирование и
                           строительство""",
            keywords="""функции технического заказчика,
                        строительный контроль,
                        проектирование,
                        строительство""",
            caption=False,
        ))
        return context


class ContactPageView(TemplateView):
    template_name = 'www/content/contact.html'

    def get_context_data(self, **kwargs):
        context = super(ContactPageView, self).get_context_data(**kwargs)
        context.update(dict(
            schema={
                'page': 'ContactPage',
            },
            title='Контакты',
            description='Контактная информация группы компаний «ССК»'
        ))
        return context


class PrivacyPageView(TemplateView):
    template_name = 'www/content/privacy.html'

    def get_context_data(self, **kwargs):
        context = super(PrivacyPageView, self).get_context_data(**kwargs)
        context.update(dict(
            title='Политика конфиденциальности',
            description='Политика конфиденциальности сайта Группы компаний «ССК»',
        ))
        return context


class InfoPageView(TemplateView):
    template_name = 'www/content/info.html'

    def get_context_data(self, **kwargs):
        context = super(InfoPageView, self).get_context_data(**kwargs)
        context.update(dict(
            robots='noindex,nofollow,noarchive',
            title='Раскрываемая информация',
        ))
        return context
