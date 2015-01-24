from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^', include('photo_geoip.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^', TemplateView.as_view(template_name="index.html")),

)
