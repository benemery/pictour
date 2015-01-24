from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView
from django.views.generic import View
import json
import requests

def home(request):
    context = {
        'redirect_url': settings.REDIRECT_URL + 'dbresponse',
        'app_key': settings.DROPBOX_APP_KEY,
    }
    print context
    return render_to_response( 'index.html', context, context_instance=RequestContext(request))
    return render(request, 'index.html', context)


# class IndexView(TemplateView):
#     template_name="index.html"

#     def get_context_data(self, **kwargs):
#         context = super(IndexView, self).get_context_data(**kwargs)
    
#         print context
#         return context

class DBResponseView(View):
    def get(self, request):
        payload = {
            'code':request.GET.get('code', ''),
            'grant_type':'authorization_code',
            'redirect_uri':settings.REDIRECT_URL + 'dbresponse',
        }
        response = requests.post('https://api.dropbox.com/1/oauth2/token',
                   data=payload,
                   auth=(settings.DROPBOX_APP_KEY, settings.DROPBOX_APP_SECRET))
        responseJson = json.loads(response.text)
        access_token = responseJson['access_token']
        user_id = responseJson['uid']

        accountInfoRequestHeaders = {
            'Authorization': 'Bearer ' + access_token
        }
        accountInfoReponse = requests.post('https://api.dropbox.com/1/account/info', headers=accountInfoRequestHeaders)
        userJson = json.loads(accountInfoReponse.text)
        name = userJson['display_name']
        email = userJson['email']
        # return HttpResponse('Yay it worked!!')

        user, _ = User.objects.get_or_create(username=email, first_name=name)

        user.set_password('password')
        user.save()

        user = authenticate(username=email, password='password')

        # Login user now!
        login(request, user)

        return HttpResponseRedirect('/your-tours/')

from badges import views
urlpatterns = patterns('',
    url(r'^', include('photo_geoip.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^dbresponse', DBResponseView.as_view(), name='dbresponse'),

    url(r'^$', home, name='home'),
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
