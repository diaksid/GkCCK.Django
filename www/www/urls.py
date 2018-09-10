from django.conf import settings
from django.conf.urls import url, include
from django.contrib.sitemaps.views import sitemap
from django.contrib import admin
# from filebrowser.sites import site as filebrowsersite

from . import views
from .sitemaps import sitemaps

admin.AdminSite.site_title = 'GkCCK админ'
admin.AdminSite.site_header = 'GkCCK администрирование'

handler400 = views.http400
handler403 = views.http403
handler404 = views.http404
handler500 = views.http500

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(),
        name='home'),

    url(r'^about$', views.AboutPageView.as_view(),
        name='about'),
    url(r'^contact$', views.ContactPageView.as_view(),
        name='contact'),
    url(r'^privacy$', views.PrivacyPageView.as_view(),
        name='privacy'),
    url(r'^info$', views.InfoPageView.as_view()),

    # url(r'^news',
    #     include('apps.news.urls', namespace='news')),
    url(r'^permits',
        include('apps.permits.urls', namespace='permits')),
    url(r'^activities',
        include('apps.activities.urls', namespace='activities')),
    url(r'^objects',
        include('apps.objects.urls', namespace='objects')),

    url(r'^partners$', views.PartnersJSONAjaxView.as_view()),

    url(r'^postbox',
        include('proj.postbox.urls', namespace='postbox')),
    # url(r'^callback',
    #     include('proj.callback.urls', namespace='callback')),

    url(r'^robots\.txt$', views.RobotsView.as_view()),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps()},
        name='django.contrib.sitemaps.views.sitemap'),

    # url(r'^admin/doc/',
    #     include('django.contrib.admindocs.urls')),
    # url(r'^admin/filebrowser/',
    #     include(filebrowsersite.urls)),
    url(r'^grappelli/',
        include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
