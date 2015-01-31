from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from badges import views

urlpatterns = patterns('',
    url(r'^', include('photo_geoip.urls')),

    url(r'^admin/', include(admin.site.urls)),

)

urlpatterns += patterns('badges',
    url(r'^$', views.overview, name="badges_overview"),
    url(r'^(?P<slug>[A-Za-z0-9_-]+)/$', views.detail, name="badge_detail"),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
