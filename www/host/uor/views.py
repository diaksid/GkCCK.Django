from django.views.defaults import (bad_request, permission_denied,
                                   page_not_found, server_error)
from django.views.generic.base import TemplateView


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
    template_name = 'proj/robots.html'


class HomePageView(TemplateView):
    template_name = 'uor/content/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context.update(dict(
            title='Управление отделочных работ',
            name='Управление Отделочных Работ',
            description="""Управления Отделочных Работ Группы Компаний «ССК» предлагает услуги по
                           ремонту, монтажу, отделке, проектированию и дизайну""",
            keywords="""отделочные работы,
                        монтаж систем,
                        проектирование,
                        дизайн""",
            breadcrumbs=False,
        ))
        return context


class PrivacyPageView(TemplateView):
    template_name = 'uor/content/privacy.html'

    def get_context_data(self, **kwargs):
        context = super(PrivacyPageView, self).get_context_data(**kwargs)
        context.update(dict(
            title='Политика конфиденциальности',
            description='Политика конфиденциальности сайта Группы компаний «ССК»',
        ))
        return context


class FinishPageView(TemplateView):
    template_name = 'uor/content/finish.html'

    def get_context_data(self, **kwargs):
        context = super(FinishPageView, self).get_context_data(**kwargs)
        context.update(dict(
            title='Отделочные работы',
            description="""Управления Отделочных Работ ГК «ССК» выполняет отделочные работы на уровне
                           косметического ремонта, ремонта эконом класса,
                           евроремонта или элитного ремонта""",
            keywords="""отделочная работа,
                        косметический ремонт,
                        евроремонт,
                        элитный ремонт""",
            caption='УОР ГК «ССК»',
        ))
        return context


class InstallPageView(TemplateView):
    template_name = 'uor/content/install.html'

    def get_context_data(self, **kwargs):
        context = super(InstallPageView, self).get_context_data(**kwargs)
        context.update(dict(
            title='Монтаж конструкций, систем и сетей',
            description="""Управления Отделочных Работ ГК «ССК» выполняет монтаж натяжных потолков,
                           систем кондиционирования, систем вентиляции и канализации,
                           электрических сетей""",
            keywords="""монтаж,
                        натяжной потолок,
                        кондиционирование,
                        система вентиляции,
                        система канализации,
                        электрическя сеть,
                        умный дом""",
            caption='УОР ГК «ССК»',
        ))
        return context


class ProjectPageView(TemplateView):
    template_name = 'uor/content/project.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectPageView, self).get_context_data(**kwargs)
        context.update(dict(
            title='Дизайн и проектирование',
            description="""Управления Отделочных Работ ГК «ССК» выполняет
                           все виды проектных и дизайнерских работ""",
            keywords="""проект,
                        дизайн,
                        проектная работа""",
            caption='УОР ГК «ССК»',
        ))
        return context


class ContactPageView(TemplateView):
    template_name = 'uor/content/contact.html'

    def get_context_data(self, **kwargs):
        context = super(ContactPageView, self).get_context_data(**kwargs)
        context.update(dict(
            schema={
                'page': 'ContactPage',
            },
            title='Контакты',
            description='Контактная информация группы компаний «ССК»',
        ))
        return context
