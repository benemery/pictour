from django.contrib import admin

from photo_geoip.models import Tour, Step, UserAuthTokens

admin.site.register(Tour)
admin.site.register(Step)
admin.site.register(UserAuthTokens)
