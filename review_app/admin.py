from django.contrib import admin
from review_app.models import Profile, FarmersMarket, Vendor, VendorType, Rating
# Register your models here.


admin.site.register(Profile)
admin.site.register(VendorType)
admin.site.register(Vendor)
admin.site.register(FarmersMarket)
admin.site.register(Rating)
