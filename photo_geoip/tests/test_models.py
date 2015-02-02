import os

from django_any import any_model
from django.core.files import File

from photo_geoip.models import Step, Tour, UserTour, UserStep
from photo_geoip.tests.helpers import BASE_DIR, create_tour
import pytest

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

        path = os.path.join(BASE_DIR, "test_image_1.jpg")
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

    def test_mark_complete(self):
        """Does marking a tour as complete behave as expected?"""
        tour = create_tour()
        user_tour = any_model(UserTour, tour=tour, active=True, completed=False)

        assert user_tour.active
        assert not user_tour.completed

        user_tour.mark_completed()
        assert not user_tour.active
        assert user_tour.completed

@pytest.mark.django_db
class TestModelTour():
    def test_compelted_count(self):
        """Does our completed count logic work?"""
        tour1 = any_model(Tour, image=None, name="Tour #1")
        tour2 = any_model(Tour, image=None, name="Tour #2")

        any_model(UserTour, tour=tour1, completed=True)
        any_model(UserTour, tour=tour1, completed=True)
        any_model(UserTour, tour=tour1, completed=True)
        any_model(UserTour, tour=tour1, completed=False)

        assert tour1.completed_count == 3
        assert tour2.completed_count == 0

    def test_active_count(self):
        """Does our active count logic work?"""
        tour = any_model(Tour, image=None, name="My Tour")

        any_model(UserTour, tour=tour, completed=True, active=True)
        any_model(UserTour, tour=tour, completed=False, active=True)
        any_model(UserTour, tour=tour, completed=True, active=False)

        assert tour.active_count == 1
