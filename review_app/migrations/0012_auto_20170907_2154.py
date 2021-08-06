# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-09-07 21:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ("review_app", "0011_auto_20160731_1737"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile_fm_like",
            field=models.ManyToManyField(
                blank=True, related_name="fm_likes", to="review_app.FarmersMarket"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="profile_vendor_like",
            field=models.ManyToManyField(
                blank=True, related_name="vendor_likes", to="review_app.Vendor"
            ),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="at_farmers_market",
            field=models.ManyToManyField(
                to="review_app.FarmersMarket", verbose_name="Located here"
            ),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="vendor_banner_picture",
            field=models.ImageField(
                blank=True, upload_to="vendor_images", verbose_name="Banner Picture"
            ),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="vendor_contact_email",
            field=models.EmailField(max_length=254, verbose_name="Email"),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="vendor_contact_name",
            field=models.CharField(max_length=50, verbose_name="Contact Name"),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="vendor_description",
            field=models.TextField(blank=True, verbose_name="Description"),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="vendor_name",
            field=models.CharField(max_length=100, verbose_name="Vendor Name"),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="vendor_phone",
            field=localflavor.us.models.PhoneNumberField(
                blank=True, verbose_name="Phone"
            ),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="vendor_picture",
            field=models.ImageField(
                blank=True, upload_to="vendor_images", verbose_name="Profile Picture"
            ),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="vendor_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="review_app.VendorType",
                verbose_name="Catergory",
            ),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="vendor_website",
            field=models.URLField(blank=True, verbose_name="Website"),
        ),
    ]
