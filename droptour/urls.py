from django.conf import settings
from django.conf.urls import patterns, include, url
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import View
from django.contrib import admin
from settings_local import DROPBOX_APP_KEY, DROPBOX_APP_SECRET, REDIRECT_URL
import json
import requests

class IndexView(TemplateView):
    template_name="index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['redirect_url'] = REDIRECT_URL + 'dbresponse'
        context['app_key'] = DROPBOX_APP_KEY
        return context
    
class DBResponseView(View):
    def get(self, request): 
        payload = {
            'code':request.GET.get('code', ''),
            'grant_type':'authorization_code',
            'redirect_uri':REDIRECT_URL + 'dbresponse',
        }
        response = requests.post('https://api.dropbox.com/1/oauth2/token', data=payload, auth=(DROPBOX_APP_KEY, DROPBOX_APP_SECRET))
        responseJson = json.loads(response.text)
        access_token = responseJson['access_token']
        user_id = responseJson['uid']

        accountInfoRequestHeaders = {
            'Authorization': 'Bearer ' + access_token
        }
        accountInfoReponse = requests.post('https://api.dropbox.com/1/account/info', headers=accountInfoRequestHeaders)
        userJson = json.loads(accountInfoReponse.text)
        name = user['display_name']
        email = user['email']
        return HttpResponse('Yay it worked!!')


urlpatterns = patterns('',
    url(r'^', include('photo_geoip.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^dbresponse', DBResponseView.as_view(), name='dbresponse'),

    url(r'^', IndexView.as_view()),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
