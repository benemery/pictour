import os

from django_any import any_model
from django.core.files import File

from photo_geoip.models import Step, Tour, UserTour, UserStep
import pytest

CURRENT_DIR = os.path.dirname(__file__)

@pytest.mark.django_db
class TestModelSteps():
    def test_next(self):
        """Does our next function work?"""
        tour = any_model(Tour, image=None, name='My Test Tour')
        any_model(Step, tour=tour, step_number=1)
        any_model(Step, tour=tour, step_number=2)
        any_model(Step, tour=tour, step_number=3)

        first = tour.first_step
        assert first.step_number == 1

        second = first.next()
        assert second.step_number == 2

        third = second.next()
        assert third.step_number == 3

        fourth = third.next()
        assert fourth == None

@pytest.mark.django_db
class TestModelUserStep():
    def test_image(self):
        """Can we save an image?"""
        tour = any_model(Tour, image=None, name='My Test Tour')
        step = any_model(Step, tour=tour, step_number=1)

        ut = any_model(UserTour, tour=tour)

        path = os.path.join(CURRENT_DIR, "test_image_1.jpg")
        with open(path, 'rb') as fin:
            f = File(fin)
            us = UserStep(user_tour=ut, step=step, image='')
            us.image.save('1.jpg', f)

@pytest.mark.django_db
class TestModelUserTour():
    def test_percentage_completion(self):
        tour = any_model(Tour, image=None, name='My Test Tour')
        step1 = any_model(Step, tour=tour, step_number=1)
        step2 = any_model(Step, tour=tour, step_number=2)
        step3 = any_model(Step, tour=tour, step_number=3)

        user_tour = any_model(UserTour, tour=tour)
        any_model(UserStep, user_tour=user_tour, step=step1, image='')

        assert user_tour.percentage_completion == 33