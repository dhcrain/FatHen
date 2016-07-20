from django.db import models
from django.template.defaultfilters import slugify
from autoslug import AutoSlugField
from localflavor.us.models import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    FARMERS_MARKET = 'Farmers Market'
    VENDOR = 'Vendor'
    REVIEWER = 'Reviewer'
    user_type_choices = ((FARMERS_MARKET, 'Farmers Market'), (VENDOR, 'Vendor'), (REVIEWER, 'Reviewer'))
    profile_user = models.OneToOneField('auth.User')
    user_type = models.CharField(max_length=15, choices=user_type_choices)
    profile_picture = models.ImageField(upload_to="profile_images", blank=True)

    def __str__(self):
        return str(self.profile_user)

    @property
    def profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        else:
            return "http://www.sessionlogs.com/media/icons/defaultIcon.png"



class VendorType(models.Model):
    vendor_type = models.CharField(max_length=30)

    def __str__(self):
        return self.vendor_type


class FarmersMarket(models.Model):
    fm_name = models.CharField(max_length=100)
    # https://pypi.python.org/pypi/django-autoslug
    fm_slug = AutoSlugField(populate_from='fm_name', unique=True, editable=True, blank=True)
    fm_description = models.TextField(blank=True)
    fm_picture = models.ImageField(upload_to="fm_images", blank=True)
    fm_banner_picture = models.ImageField(upload_to="fm_images", blank=True)
    fm_contact_name = models.CharField(max_length=30)
    fm_contact_email = models.EmailField()
    fm_website = models.URLField(blank=True)
    OPEN_AIR = 'Open-Air'
    OA_COVERED = 'Open-Air/Covered'
    facility_choices = ((OPEN_AIR, 'Open-Air'), (OA_COVERED, 'Open-Air/Covered'))
    fm_facility_type = models.CharField(max_length=30, blank=True, choices=facility_choices)
    fm_county = models.CharField(max_length=20, blank=True)
    fm_address = models.CharField(max_length=30, blank=True)
    fm_programs_accepted = models.CharField(max_length=30, blank=True)
    # https://pypi.python.org/pypi/django-localflavor
    fm_phone = PhoneNumberField(blank=True)
    fm_hrs_of_operation = models.CharField(max_length=30, blank=True)
    fm_seasons_of_operation = models.CharField(max_length=30, blank=True)
    fm_handicap_accessible = models.CharField(max_length=30, blank=True)
    fm_iframe_url = models.URLField(blank=True)
    fm_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fm_name


class Vendor(models.Model):
    at_farmers_market = models.ManyToManyField("FarmersMarket")
    vendor_name = models.CharField(max_length=100)
    # https://pypi.python.org/pypi/django-autoslug
    vendor_slug = AutoSlugField(populate_from='fm_name', unique=True, editable=True)
    vendor_description = models.TextField(blank=True)
    vendor_picture = models.ImageField(upload_to="vendor_images", blank=True)
    vendor_banner_picture = models.ImageField(upload_to="vendor_images", blank=True)
    vendor_contact_name = models.CharField(max_length=30)
    vendor_contact_email = models.EmailField()
    vendor_website = models.URLField(blank=True)
    # https://pypi.python.org/pypi/django-localflavor
    vendor_phone = PhoneNumberField(blank=True)
    vendor_type = models.ForeignKey(VendorType, blank=True, null=True)
    vendor_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name


class Rating(models.Model):
    # would like a way to limit it to one rating per user per Vendor/FarmersMarket
    rating_user = models.ForeignKey('auth.User')
    rating_vendor = models.ForeignKey(Vendor, null=True, blank=True)
    rating_fm = models.ForeignKey(FarmersMarket, null=True, blank=True)
    rating_picture = models.ImageField(upload_to="rating_images", blank=True)
    rating = models.PositiveIntegerField() # choices? 1-5?
    rating_comment = models.TextField()
    rating_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating_user)


@receiver(post_save, sender='auth.User')
def create_user_profile(**kwargs):
    created = kwargs.get("created")
    instance = kwargs.get("instance")
    if created:
        Profile.objects.create(profile_user=instance)
