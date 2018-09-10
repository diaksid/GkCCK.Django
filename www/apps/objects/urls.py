from django.conf.urls import url

from . import views

app_name = 'objects'

urlpatterns = [
    url(r'^$', views.ObjectListView.as_view(), name='list'),
    url(r'^/(?P<slug>.+)$', views.ObjectDetailView.as_view(), name='detail'),
]
