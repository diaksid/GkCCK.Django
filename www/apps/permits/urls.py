from django.conf.urls import url

from . import views

app_name = 'permits'

urlpatterns = [
    url(r'^$', views.PermitListView.as_view(), name='list'),
    url(r'^/(?P<owner>.+)/(?P<slug>.+)$', views.PermitDetailView.as_view(), name='detail'),
    url(r'^/(?P<owner>.+)$', views.PermitListView.as_view(), name='list'),
]
