import os

from django.core.urlresolvers import reverse
from django.test import TestCase

from django_any import any_model
from photo_geoip.models import Tour, Step
from photo_geoip.helpers import extract_data, haversine, image_within_limit




CURRENT_DIR = os.path.dirname(__file__)

# Create your tests here.
class TestGeoDataExtraction(TestCase):
    def test_lon_lat(self):
        """Can we extract location data"""
        path = os.path.join(CURRENT_DIR, "test_image_1.jpg")
        with open(path, 'rb') as fin:
            lat, lon = extract_data(fin)
            self.assertEqual(lat, 51.524575)
            self.assertEqual(lon, -0.07884722222222222)

class TestImageLimit(TestCase):
    def test_within_boundary(self):
        """Can we compare to lon / lats?"""
        path = os.path.join(CURRENT_DIR, "test_image_1.jpg")
        with open(path, 'rb') as fin:
            lat2 = 51.52534
            lon2 = -0.07754
            self.assertTrue(image_within_limit(lat2, lon2, fin))

class TestModelSteps(TestCase):
    def test_next(self):
        """Does our next function work?"""
        tour = any_model(Tour, name='My Test Tour')
        any_model(Step, tour=tour, step_number=1)
        any_model(Step, tour=tour, step_number=2)
        any_model(Step, tour=tour, step_number=3)

        first = tour.first_step
        self.assertEqual(first.step_number, 1)

        second = first.next()
        self.assertEqual(second.step_number, 2)

        third = second.next()
        self.assertEqual(third.step_number, 3)

        fourth = third.next()
        self.assertEqual(fourth, -1)


class TestViewWebhook(TestCase):
    def test_get(self):
        """Do we respond to a challenge correctly?"""
        challenge = "this-is-a-challenge"
        response = self.client.get(reverse('webhook'), {'challenge': challenge})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, challenge)

    def test_post_invalid_sig(self):
        """What happens if we supply an incorrect sig?"""
        response = self.client.post(reverse('webhook'), X_Dropbox_Signature="FOOBAR")
        self.assertEqual(response.status_code, 403)
        
