from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.CallbackRedirectView.as_view(), name='send'),
]
