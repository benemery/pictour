from django.contrib import admin

from photo_geoip.models import Tour, Step, UserAuthTokens, UserTour, UserStep

class AdminTour(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }


admin.site.register(Tour, AdminTour)
admin.site.register(Step)
admin.site.register(UserAuthTokens)
admin.site.register(UserTour)
admin.site.register(UserStep)
