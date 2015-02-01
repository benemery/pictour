from math import floor

from django.db import models

class Tour(models.Model):
    """Parent model for grouping a tour."""
    name = models.CharField(max_length=256)
    punchline = models.TextField(blank=True, default='')
    slug = models.SlugField()
    image = models.ImageField(blank=True, default='')

    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    @property
    def first_step(self):
        return self.steps.get(step_number=1)

    @property
    def completed_count(self):
        """How many times has this tour been completed?"""
        return UserTour.objects.filter(tour=self, completed=True).count()

    @property
    def active_count(self):
        """How many people are currently doing this tour?"""
        return UserTour.objects.filter(tour=self, completed=False, active=True).count()

class Step(models.Model):
    """Steps for a tour"""
    name = models.CharField(max_length=256)
    clue = models.TextField()

    longitude = models.FloatField()
    latitude = models.FloatField()
    error_boundary = models.FloatField(default=0.5, help_text='How far can you be from the point (in Km)')

    tour = models.ForeignKey(to='photo_geoip.Tour', related_name='steps')
    step_number = models.IntegerField()

    def __unicode__(self):
        return self.name

    def next(self):
        """Get the next step, return None if no more"""
        base_qs = self.tour.steps.filter(step_number__gt=self.step_number)
        if not base_qs.exists():
            return
        return base_qs[:1][0]

class UserTour(models.Model):
    """Keep track of what tours a user has completed / is currently doing"""
    user = models.ForeignKey(to='auth.User', related_name='tours')
    tour = models.ForeignKey(to='photo_geoip.Tour')
    active = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)

    def get_completed_steps(self):
        return self.completed_steps.all().order_by('id')

    @property
    def current_step(self):
        """What is the current step for the user?"""
        if not self.completed_steps.exists():
            return self.tour.first_step
        last_step = self.completed_steps.all().order_by('-step__step_number')[0]
        return last_step.step.next()

    @staticmethod
    def get_user_tour(user):
        """Find this user's current tour / add them to the newest one"""
        user_tour_qs = user.tours.filter(active=True)

        if not user_tour_qs.exists():
            # This user is currently not a member of a tour!?
            # Meh, let's add em to one.
            tour = Tour.objects.all().order_by('id')[0]
            if UserTour.objects.filter(user=user, tour=tour).exists():
                # User has already completed this tour. Just return.
                return
            user_tour, _ = UserTour.objects.get_or_create(user=user, tour=tour)
        else:
            user_tour = user_tour_qs[0]

        return user_tour

    @property
    def percentage_completion(self):
        """How far through the tour is this user?"""
        all_steps = self.tour.steps.count() or 1
        completed_steps = self.completed_steps.count()
        return int(floor(float(completed_steps) / all_steps * 100))

    def mark_completed(self):
        self.active = False
        self.completed = True
        self.save()

class UserStep(models.Model):
    """Keep track of the photos users take at each step"""
    user_tour = models.ForeignKey(to='photo_geoip.UserTour', related_name='completed_steps')
    step = models.ForeignKey(to='photo_geoip.Step')
    image = models.ImageField(blank=True, null=True)

class UserAuthTokens(models.Model):
    """Keep track of oauth tokens here"""
    user = models.ForeignKey('auth.User')
    token = models.CharField(max_length=1024)
    dropbox_uid = models.IntegerField()
    cursor = models.CharField(max_length=2048, blank=True, default='')

# Ensure badges are created
from photo_geoip.meta_badges import *
