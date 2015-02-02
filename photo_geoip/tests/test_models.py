import os

from django.contrib.auth.models import User
from django.core.files import File

from django_any import any_model
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

    def test_current_step(self):
        """Does our current step functionality work?"""
        tour = create_tour()
        step1 = any_model(Step, tour=tour, step_number=1)
        step2 = any_model(Step, tour=tour, step_number=2)
        step3 = any_model(Step, tour=tour, step_number=3)

        user_tour = any_model(UserTour, tour=tour)

        assert user_tour.current_step.step_number == 1
        any_model(UserStep, user_tour=user_tour, step=step1, image='')
        assert user_tour.current_step.step_number == 2
        any_model(UserStep, user_tour=user_tour, step=step2, image='')
        assert user_tour.current_step.step_number == 3
        any_model(UserStep, user_tour=user_tour, step=step3, image='')

    def test_get_tour_not_enrolled(self):
        """Do we auto-enroll a user?"""
        tour = create_tour()
        user = any_model(User)

        assert UserTour.objects.filter(user=user).count() == 0
        UserTour.get_user_tour(user)
        # User should have been added to a tour
        assert UserTour.objects.filter(user=user).count() == 1

    def test_get_tour_enrolled(self):
        """Do we get the correct tour?"""
        tour1 = create_tour()
        tour2 = create_tour()
        user = any_model(User)
        any_model(UserTour, user=user, tour=tour1, active=False, completed=False)
        user_tour = any_model(UserTour, user=user, tour=tour2, active=True, completed=False)

        assert UserTour.get_user_tour(user) == user_tour

    def test_completed_auto_tour(self):
        """What happens if the user has completed all the tours?!"""
        tour = create_tour()
        user = any_model(User)
        any_model(UserTour, user=user, tour=tour, active=False, completed=True)

        assert UserTour.get_user_tour(user) is None


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
