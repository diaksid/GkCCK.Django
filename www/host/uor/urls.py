from django.conf import settings
from django.conf.urls import url, include
from django.contrib.sitemaps.views import sitemap

from www.urls import handler400, handler403, handler404, handler500

from . import views
from .sitemaps import sitemaps

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(),
        name='home'),

    url(r'^privacy$', views.PrivacyPageView.as_view(),
        name='privacy'),

    url(r'^finish$', views.FinishPageView.as_view(),
        name='finish'),
    url(r'^install$', views.InstallPageView.as_view(),
        name='install'),
    url(r'^project$', views.ProjectPageView.as_view(),
        name='project'),

    url(r'^contact$', views.ContactPageView.as_view(),
        name='contact'),

    url(r'^postbox',
        include('proj.postbox.urls', namespace='postbox')),
    # url(r'^callback',
    #     include('proj.callback.urls', namespace='callback')),

    url(r'^robots\.txt$', views.RobotsView.as_view()),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps()},
        name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
