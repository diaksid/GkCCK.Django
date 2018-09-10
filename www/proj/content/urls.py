from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.PageListView.as_view(), name='list'),
    url(r'^/(?P<slug>.+)$', views.PageDetailView.as_view(), name='detail'),
]
