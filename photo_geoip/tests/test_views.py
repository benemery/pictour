from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django_any import any_model
from photo_geoip.models import Tour, UserTour
import pytest

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
    def test_post_ok(self, client):
        """Do we create a user tour as expected?"""
        user = User.objects.create_user('admin', password='root')
        client.login(username='admin', password='root')
        any_model(Tour, image=None, slug='slug1')
        any_model(Tour, image=None, slug='slug2')

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
        any_model(Tour, image=None, slug='slug1')

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