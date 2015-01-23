from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View

# from flask import Flask, request, url_for
from hashlib import sha256
import hmac
import threading
import json
from dropbox.client import DropboxClient

from photo_geoip.models import UserAuthTokens

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
        return ''

def process_user(uid):
    '''Call /delta for the given user ID and process any changes.'''
    # OAuth token for the user
    user_auth = UserAuthTokens.objects.get(dropbox_uid=uid)
    token = user_auth.token

    # /delta cursor for the user (None the first time)
    cursor = user_auth.cursor

    client = DropboxClient(token)
    has_more = True

    while has_more:
        result = client.delta(cursor)

        for path, metadata in result['entries']:

            # Ignore deleted files, folders, and non-markdown files
            if (metadata is None or
                    metadata['is_dir'] or
                    not path.endswith('.jpg')):
                continue

            import time
            with open('%s.jpg' % time.time(), 'wb') as out:
                with client.get_file(path) as f:
                  out.write(f.read())

        # Update cursor
        cursor = result['cursor']

        user_auth.cursor = cursor
        user_auth.save()

        # Repeat only if there's more to do
        has_more = result['has_more']
