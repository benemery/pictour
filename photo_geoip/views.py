from hashlib import sha256
import hmac
import json
from StringIO import StringIO
import threading

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.files import File
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import View
from dropbox.client import DropboxClient
from photo_geoip.models import UserAuthTokens, UserStep, UserTour, Tour
from photo_geoip.helpers import image_within_limit
import requests

def home(request):
    context = {
        'redirect_url': reverse('dbresponse'),
        'app_key': settings.DROPBOX_APP_KEY,
    }
    return render_to_response( 'index.html', context, context_instance=RequestContext(request))

def dropbox_oauth(request):
    """Pipeline for DropBox's oAuth"""
    payload = {
        'code': request.GET.get('code', ''),
        'grant_type': 'authorization_code',
        'redirect_uri': reverse('dbresponse'),
    }
    response = requests.post('https://api.dropbox.com/1/oauth2/token',
               data=payload,
               auth=(settings.DROPBOX_APP_KEY, settings.DROPBOX_APP_SECRET))

    if not response.ok:
        response.raise_for_status()

    data = response.json()
    access_token = data['access_token']
    user_id = data['uid']


    headers = {
        'Authorization': 'Bearer %s' % access_token
    }
    response = requests.post('https://api.dropbox.com/1/account/info',
                                headers=headers)

    if not response.ok:
        response.raise_for_status()

    data = response.json()
    name = data['display_name']
    email = data['email']

    user, _ = User.objects.get_or_create(username=email, first_name=name)

    try:
        uat = UserAuthTokens.objects.get(dropbox_uid=user_id)
    except UserAuthTokens.DoesNotExist:
        uat = UserAuthTokens(dropbox_uid=user_id, user=user)
    uat.token = access_token
    uat.save()

    user = authenticate(dropbox_uid=user_id, token=access_token)

    # Login user now!
    login(request, user)

    return HttpResponseRedirect('/your-tours/')


class Webhook(View):
    def get(self, request):
        challenge = request.GET.get('challenge', '')
        return HttpResponse(challenge)

    def post(self, request):
        '''Receive a list of changed user IDs from Dropbox and process each.'''
        # Make sure this is a valid request from Dropbox
        signature = request.META.get('HTTP_X_DROPBOX_SIGNATURE', '')

        if signature != hmac.new(settings.DROPBOX_APP_SECRET, request.body, sha256).hexdigest():
            return HttpResponse(status=403)

        for uid in json.loads(request.body)['delta']['users']:
            # We need to respond quickly to the webhook request, so we do the
            # actual work in a separate thread. For more robustness, it's a
            # good idea to add the work to a reliable queue and process the queue
            # in a worker process.
            threading.Thread(target=process_user, args=(uid,)).start()
        return HttpResponse('')

def process_user(uid):
    '''Call /delta for the given user ID and process any changes.'''
    # OAuth token for the user
    user_auth = UserAuthTokens.objects.get(dropbox_uid=uid)
    token = user_auth.token

    # /delta cursor for the user (None the first time)
    cursor = user_auth.cursor

    client = DropboxClient(token)
    has_more = True

    user_tour = UserTour.get_user_tour(user_auth.user)

    if not user_tour:
        # User has already completed this tour. Just return.
        return

    current_step = user_tour.current_step

    if not current_step:
        # Completed this current tour!
        # Well done you! :D
        user_tour.mark_completed()

    while has_more:
        result = client.delta(cursor)

        for path, metadata in result['entries']:

            # Ignore deleted files, folders, and non-image files
            if (metadata is None or
                    metadata['is_dir'] or
                    not path.endswith('.jpg')):
                continue

            try:
                with client.get_file(path) as f:
                    # ewwww
                    # We're guessing the header size here.. We shouldn't.
                    s = StringIO(f.read(2048))
                    within_range = image_within_limit(
                                        current_step.longitude,
                                        current_step.latitude,
                                        image=s,
                                        error_margin=current_step.error_boundary)

                    if within_range:
                        us = UserStep(user_tour=user_tour, step=current_step)
                        us.save()

                        # Now save the image=
                        if metadata['thumb_exists']:
                            # Download the thumb instead
                            s = StringIO(client.thumbnail(path, size='l').read())
                        else:
                            # Pull the original file
                            s.write(f.read())

                        s.seek(0)
                        filename = 'step_%s.jpg' % us.id
                        us.image.save(filename, File(s))

                        # Check if complete
                        current_step = user_tour.current_step
                        if not current_step:
                            # Completed this current tour!
                            # Well done you! :D
                            user_tour.mark_completed()

            except Exception, e:
                print e

        # Update cursor
        cursor = result['cursor']

        user_auth.cursor = cursor
        user_auth.save()

        # Repeat only if there's more to do
        has_more = result['has_more']

class YourTours(View):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(YourTours, cls).as_view(**initkwargs)
        return login_required(view, login_url='/#about')

    def get(self, request):
        user = request.user
        tours = user.tours.all().select_related('completed_steps')
        return render(request, 'your_tours.html', {'tours': tours})

    def post(self, request):
        """Creating a user tour"""
        slug = request.POST.get('slug')
        tour = get_object_or_404(Tour, slug=slug)
        UserTour.objects.get_or_create(tour=tour, user=request.user)

        if request.is_ajax():
            data = {
                'status': 'success',
            }
            return HttpResponse(json.dumps(data), content_type='application/json')

        tours = request.user.tours.all().select_related('completed_steps')
        return render(request, 'your_tours.html', {'tours': tours})

def tours(request):
    """Tour list view"""
    tours = Tour.objects.all()
    return render(request, 'available_tours.html', {'tours': tours})
