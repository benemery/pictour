from django.contrib import admin

from photo_geoip.models import Tour, Step, UserAuthTokens, UserTour, UserStep

admin.site.register(Tour)
admin.site.register(Step)
admin.site.register(UserAuthTokens)
admin.site.register(UserTour)
admin.site.register(UserStep)
