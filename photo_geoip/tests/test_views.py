import os

from django.contrib.auth.models import User
from django.core.files import File
from django.core.urlresolvers import reverse

from django_any import any_model
from photo_geoip.models import Tour, UserTour, UserAuthTokens
import responses
import pytest

BASE_DIR = os.path.dirname(__file__)

def create_tour(**options):
    defaults = {
        'image': None
    }
    defaults.update(options)
    tour = any_model(Tour, **defaults)
    if "image" not in options:
        with open(os.path.join(BASE_DIR, 'test_image_1.jpg'), 'rb') as fin:
            tour.image.save('my_image.jpg', File(fin))
            tour.save()

    return tour

class TestViewWebhook():
    def test_get(self, client):
        """Do we respond to a challenge correctly?"""
        challenge = "this-is-a-challenge"
        response = client.get(reverse('webhook'), {'challenge': challenge})

        assert response.status_code == 200
        assert response.content == challenge

    def test_post_invalid_sig(self, client):
        """What happens if we supply an incorrect sig?"""
        response = client.post(reverse('webhook'), X_Dropbox_Signature="FOOBAR")
        assert response.status_code == 403


@pytest.mark.django_db
class TestYourToursView():
    def test_get(self, client):
        """Can we load the page ok?"""
        User.objects.create_user('admin', password='root')
        client.login(username='admin', password='root')
        tour = any_model(Tour, image=None, slug='slug1')
        any_model(UserTour, tour=tour)

        response = client.get(reverse('your_tours'))
        assert response.status_code == 200

    def test_post_ok(self, client):
        """Do we create a user tour as expected?"""
        user = User.objects.create_user('admin', password='root')
        client.login(username='admin', password='root')
        create_tour(slug='slug1')
        create_tour(slug='slug2')

        # Do a full post request
        response = client.post(reverse('your_tours'), {'slug': 'slug1'})
        assert response.status_code == 200
        assert user.tours.count() == 1

        # Do a ajax request
        response = client.post(reverse('your_tours'), {'slug': 'slug2'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        assert user.tours.count() == 2

    def test_post_duplicate(self, client):
        """What happens if we attempt multiple enrolments?"""
        user = User.objects.create_user('admin', password='root')
        client.login(username='admin', password='root')
        create_tour(slug='slug1')

        response = client.post(reverse('your_tours'), {'slug': 'slug1'})
        response = client.post(reverse('your_tours'), {'slug': 'slug1'})

        assert response.status_code == 200
        assert user.tours.count() == 1

    def test_post_unknown_slug(self, client):
        """What happens if we don't know the slug?"""
        User.objects.create_user('admin', password='root')
        client.login(username='admin', password='root')
        any_model(Tour, image=None, slug='slug1')

        response = client.post(reverse('your_tours'), {'slug': 'FOOBAR'})
        assert response.status_code == 404

    def test_unauthenticated_user(self, client):
        """What happens if you're not authenticated?"""
        response = client.post(reverse('your_tours'), {'slug': 'FOOBAR'})
        assert response.status_code == 302

@pytest.mark.django_db
class TestHomeView():
    def test_ok(self, client):
        """Does the home page work?"""
        response = client.get(reverse('home'))
        assert response.status_code == 200

@pytest.mark.django_db
class TestDropboxOauthView():
    def _register_dropbox_responses(self):
        responses.add(responses.POST, 'https://api.dropbox.com/1/oauth2/token',
              body='{"access_token": "foobar", "uid": 1234}', status=200,
              content_type='application/json')

        responses.add(responses.POST, 'https://api.dropbox.com/1/account/info',
              body='{"display_name": "A User", "email": "someone@foo.com"}', status=200,
              content_type='application/json')

    @responses.activate
    def test_ok(self, client):
        """Does the oath pipeline work?"""
        self._register_dropbox_responses()
        response = client.get(reverse('dbresponse'))

        # Is the user now authenticated?
        assert '_auth_user_id' in client.session
        assert UserAuthTokens.objects.count() == 1
