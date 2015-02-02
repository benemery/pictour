import os

from django.core.files import File

from django_any import any_model
from photo_geoip.models import Tour

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