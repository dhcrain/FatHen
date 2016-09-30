# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-20 12:50
from __future__ import unicode_literals

from django.db import migrations
import csv
from django.template.defaultfilters import slugify


def fm_data_migrate(apps, schema_editor):
    FarmersMarket = apps.get_model("review_app", "FarmersMarket")
    with open("review_app/data/sc_farmers_markets2.csv") as infile:
        farmers_market = csv.reader(infile)
        for row in farmers_market:
            fm_slug = slugify(row[0])
            print(fm_slug)
            FarmersMarket.objects.create(fm_name=row[0], fm_slug=fm_slug, fm_contact_name=row[1],
            fm_contact_email=row[2], fm_facility_type=row[3], fm_county=row[4],
            fm_address=row[5], fm_programs_accepted=row[6], fm_phone=row[7],
            fm_website=row[8], fm_hrs_of_operation=row[10], fm_seasons_of_operation=row[11],
            fm_handicap_accessible=row[12], fm_iframe_url=row[13]
            )
    # raise Exception("2 yay")

def verndor_type_import(apps, schema_editor):
    VendorType = apps.get_model("review_app", "VendorType")
    with open("review_app/data/vendor_types.csv") as infile:
        vendor_types = csv.reader(infile)
        for row in vendor_types:
            VendorType.objects.create(vendor_type=row[1])

    # raise Exception("1 yay")

class Migration(migrations.Migration):

    dependencies = [
        ('review_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fm_data_migrate),
        migrations.RunPython(verndor_type_import),
    ]
