from hashlib import sha256
import hmac
import json
from StringIO import StringIO
import threading

from django.conf import settings
from django.core.files import File
from django.http import HttpResponse
from django.views.generic import View

from dropbox.client import DropboxClient
from photo_geoip.models import UserAuthTokens, UserStep, UserTour, Tour
from photo_geoip.helpers import image_within_limit

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

    user_tour_qs = user_auth.user.tours.filter(active=True)

    if not user_tour_qs.exists():
        # This user is currently not a member of a tour!?
        # Meh, let's add em to one.
        tour = Tour.objects.all().order_by('-id')[0]
        if UserTour.objects.filter(user=user_auth.user, tour=tour).exists():
            # User has already completed this tour. Just return.
            return
        user_tour, _ = UserTour.objects.get_or_create(user=user_auth.user, tour=tour)
    else:
        user_tour = user_tour_qs[0]

    current_step = user_tour.current_step

    if current_step == -1:
        # Completed this current tour!
        # Well done you! :D
        user_tour.active = False
        user_tour.complete = True
        user_tour.save()

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
                    # Perhaps we can just read the headers? Then if it's within
                    # range pull the entire file.
                    s = StringIO(f.read())
                    within_range = image_within_limit(
                                        current_step.longitude,
                                        current_step.latitude,
                                        image=s,
                                        error_margin=current_step.error_boundary)

                    if within_range:
                        us = UserStep(user_tour=user_tour, step=current_step)
                        us.save()

                        # Now save the image
                        s.seek(0)
                        us.image.save('%s.jpg' % us.id, File(s))
            except Exception, e:
                print e

        # Update cursor
        cursor = result['cursor']

        user_auth.cursor = cursor
        user_auth.save()

        # Repeat only if there's more to do
        has_more = result['has_more']
