from django.contrib import admin
from review_app.models import Profile, FarmersMarket, Vendor, VendorType, Status
# Register your models here.


admin.site.register(Profile)
admin.site.register(VendorType)
admin.site.register(Vendor)


class StatusAdmin(admin.ModelAdmin):
    list_display = ('status_comment', 'status_user', 'status_vendor', 'status_fm', 'status_present')

admin.site.register(Status, StatusAdmin)


class FarmersMarketAdmin(admin.ModelAdmin):
    list_display = ('fm_name', 'fm_county')
    search_fields = ['fm_name']

admin.site.register(FarmersMarket, FarmersMarketAdmin)
