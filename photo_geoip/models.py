from django.db import models

class Tour(models.Model):
    """Parent model for grouping a tour."""
    name = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

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

    def __unicode__(self):
        return self.name

    def next(self):
        """Get the next step, return -1 if no more"""
        base_qs = self.tour.steps.filter(step_number__gt=self.step_number)
        if not base_qs.exists():
            return -1
        return base_qs[:1][0]

class UserTour(models.Model):
    """Keep track of what tours a user has completed / is currently doing"""
    user = models.ForeignKey(to='auth.User', related_name='tours')
    tour = models.ForeignKey(to='photo_geoip.Tour')
    active = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)

    @property
    def current_step(self):
        """What is the current step for the user?"""
        if not self.completed_steps.exists():
            return self.tour.first_step

        print self.completed_steps.all().order_by('-step__step_number')
        last_step = self.completed_steps.all().order_by('-step__step_number')[0]
        return last_step.next()

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
