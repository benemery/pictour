import badges
from photo_geoip.models import UserTour

class TourTaker(badges.MetaBadge):
    id = "tourcompleted"
    model = UserTour
    one_time_only = True

    title = "TourTaker"
    description = "Completed the a Tour"
    level = "1"

    progress_start = 0
    progress_finish = 1

    def get_user(self, instance):
        return instance.user

    def get_progress(self, user):
        tour = UserTour.objects.filter(user=user, complete=True)
        print tour.exists()
        return 1 if tour.exists() else 0
