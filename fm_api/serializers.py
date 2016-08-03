from rest_framework import serializers
from review_app.models import FarmersMarket, Vendor


class FarmersMarketSerializer(serializers.ModelSerializer):

    class Meta:
        model = FarmersMarket
        fields = ['id', 'fm_name', 'fm_description', 'fm_picture_url', 'fm_banner_picture_url',
                  'fm_contact_name', 'fm_contact_email', 'fm_website', 'fm_facility_type',
                  'fm_county', 'fm_address', 'fm_lat', 'fm_long', 'fm_programs_accepted',
                  'fm_phone', 'fm_seasons_of_operation', 'fm_handicap_accessible', 'fm_updated']


class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = ['id', 'at_farmers_market', 'vendor_name', 'vendor_description', 'vendor_contact_name',
                  'vendor_contact_email', 'vendor_website', 'vendor_phone', 'vendor_type',
                  'vendor_picture_url', 'vendor_banner_picture_url', 'vendor_updated']
