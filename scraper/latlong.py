from models import FarmersMarket
import requests


fm_obj = FarmersMarket.objects.all()

for fm in fm_obj:
    print(fm.fm_address)


# g = geocoder.google(location.fm_address)
# print(g)
# lat = g.latlng[0]
# lng = g.latlng[1]


# google_geocode_api = os.environ['google_geocode_api']
# geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(location.fm_address, google_geocode_api)
# geocode_data = requests.get(geocode_url).text
# print(geocode_data)
