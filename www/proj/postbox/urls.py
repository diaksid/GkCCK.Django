from django.conf.urls import url

from . import views

app_name = 'postbox'

urlpatterns = [
    url(r'^$', views.PostboxRedirectView.as_view(), name='send'),
]
