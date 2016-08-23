def tr_vendor_import(apps, schema_editor):
    Vendor = apps.get_model("review_app", "Vendor")
    with open("review_app/data/tr_vendors.csv") as infile:
        tr_vendors = csv.reader(infile)
        fm = FarmersMarket.objects.get(fm_name="Travelers Rest Farmers Market")
        for row in tr_vendors:
            vendor_slug = slugify(row[1])
            vendor_type = VendorType.objects.get(id=row[0])
            Vendor.objects.create(at_farmers_market=fm, vendor_name=row[1],
            vendor_slug=vendor_slug, vendor_description=row[2], vendor_type=vendor_type
            )

    raise Exception("2 yay")

migrations.RunPython(tr_vendor_import),
