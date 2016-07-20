from django.contrib import admin
from review_app.models import Profile, FarmersMarket, Vendor, VendorType, Rating
# Register your models here.


admin.site.register(Profile)
admin.site.register(VendorType)
admin.site.register(Vendor)
admin.site.register(Rating)


class FarmersMarketAdmin(admin.ModelAdmin):
    list_display = ('fm_name', 'fm_county')
    search_fields = ['fm_name']

admin.site.register(FarmersMarket, FarmersMarketAdmin)
