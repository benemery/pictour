from django.conf.urls import patterns, include, url
from photo_geoip.views import Webhook

urlpatterns = patterns('',
    url(r'^webhook/$', Webhook.as_view(), name='webhook'),
)