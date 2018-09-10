from django.conf.urls import url

from . import views

app_name = 'activities'

urlpatterns = [
    url(r'^$', views.ActivityListView.as_view(), name='list'),
    url(r'^/(?P<activity>.+)/(?P<slug>.+)$', views.ActivityArticleView.as_view(), name='content'),
    url(r'^/(?P<slug>.+)$', views.ActivityDetailView.as_view(), name='detail'),
]
