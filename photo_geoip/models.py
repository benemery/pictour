from django.db import models

class Tour(models.Model):
    """Parent model for grouping a tour."""
    name = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def first_step(self):
        return self.steps.get(step_number=1)

class Step(models.Model):
    """Steps for a tour"""
    name = models.CharField(max_length=256)
    clue = models.TextField()

    longitude = models.FloatField()
    latitude = models.FloatField()
    error_boundary = models.FloatField(default=0.5, help_text='How far can you be from the point (in Km)')

    tour = models.ForeignKey(to='photo_geoip.Tour', related_name='steps')
    step_number = models.IntegerField()

    def next(self):
        """Get the next step, return -1 if no more"""
        base_qs = self.tour.steps.filter(step_number__gt=self.step_number)
        if not base_qs.exists():
            return -1
        return base_qs[:1][0]

class UserAuthTokens(models.Model):
    """Keep track of oauth tokens here"""
    user = models.ForeignKey('auth.User')
    token = models.CharField(max_length=1024)
