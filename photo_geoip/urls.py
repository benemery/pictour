from django.conf.urls import patterns, include, url
from photo_geoip.views import Webhook, YourTours, dropbox_oauth, home, tours

urlpatterns = patterns('',
    url(r'^webhook/$', Webhook.as_view(), name='webhook'),
    url(r'^tours/$', tours, name='tours'),
    url(r'^your-tours/$', YourTours.as_view(), name='your_tours'),
    url(r'^dbresponse', dropbox_oauth, name='dbresponse'),
    url(r'^$', home, name='home'),
)