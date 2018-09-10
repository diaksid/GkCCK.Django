from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.ArticleListView.as_view(), name='list'),
    url(r'^/(?P<year>[0-9]{4})$', views.ArticleListView.as_view(), name='list.year'),
    url(r'^/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})$', views.ArticleListView.as_view(), name='list.month'),
    url(r'^/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})$', views.ArticleListView.as_view(), name='list.day'),
    url(r'^/(?P<slug>.+)$', views.ArticleDetailView.as_view(), name='detail'),
]
