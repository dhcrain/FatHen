import requests
from bs4 import BeautifulSoup
import geocoder
import csv
import datetime
import re
from io import open as iopen

start_time = datetime.datetime.now()
print(start_time)


def requests_image(file_url, file_name):
    suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg', ]
    file_suffix = file_name.split('.')[1]
    i = requests.get(file_url)
    if file_suffix in suffix_list and i.status_code == requests.codes.ok:
        with iopen(file_name, 'wb') as file:
            file.write(i.content)
    else:
        return False

with open("mi_farmers_markets.csv", "w", newline="") as outfile:
    page_size = 2000
    url = "http://www.michigan.org/api/properties/geojson/random/-90.24169921875,42.93229601903058,-79.991455078125,45.90529985724799/137?page=0&pagesize={}&c=44.4377:-85.1166:7".format(page_size)
    content = requests.get(url).json()
    # souper = BeautifulSoup(content, "html.parser")
    print(len(content["features"]))
    for fm in content["features"]:
        fm_name = fm["properties"]["plainTitle"].replace("&amp;", "&").replace("&#039;", "'").replace("’", "'").replace("`", "'").strip()
        print(fm_name)

        rendered_content = fm['properties']['renderedContent']
        content_html = BeautifulSoup(rendered_content, "html.parser")
        img_link = content_html.find('img', class_='img-responsive')
        file_name = ""
        if img_link is not None:
            img_url = 'http:' + img_link.attrs['src'].replace('ar_5:4,c_fill,w_200,g_face,q_50/', '')
            file_name = fm_name.replace(' ', '_').replace(',', '').replace("'", "").replace("/", "").lower() + '.jpg'
            print(file_name)
            print(img_url)
            requests_image(img_url, file_name)

        fm_lat = fm["geometry"]["coordinates"][0]
        fm_long = fm["geometry"]["coordinates"][1]

        detail_url = BeautifulSoup(fm["properties"]["renderedContent"], "html.parser").find("article").attrs["about"]
        detail = requests.get("http://www.michigan.org" + detail_url).text
        detail_soup = BeautifulSoup(detail, "html.parser")
        try:
            fm_contact_email = detail_soup.find("a", class_="email--business").attrs["href"].split(":")[1].strip()
        except Exception as e:
            # print(e)
            fm_contact_email = ""

        fm_description = detail_soup.find("div", property="content:encoded").text.replace("\n", "").strip()
        # print(fm_description)

        try:
            season_0 = re.split("open", fm_description, flags=re.IGNORECASE)[1].strip()
            # print(season_0)
            season = season_0.split(".")[0].strip()
            # season = fm_description.split("open")[1].split(".")[0]
            # print(season)
        except Exception as e:
            # print(e)
            season = ""
        try:
            fm_phone = detail_soup.find("a", class_="phone--link").text.strip()
        except Exception as e:
            fm_phone = ""
        street_address = detail_soup.find("span", class_="address").text.strip()
        city_st_zip = detail_soup.find("span", class_="city-state-zip").text.strip()
        mrkt_address = street_address + city_st_zip
        # print(mrkt_address)
        g = geocoder.google(mrkt_address)
        fm_addr = g.address
        # print(fm_addr)
        try:
            street = g.housenumber + " " + g.street
        except Exception as e:
            street = g.street
        city = g.city
        if city is None:
            print(g.content)
            try:
                city_results = g.content['results'][0]['address_components']
                for r in city_results:
                    city_name = r['long_name']
                    if "Township" in city_name:
                        city = city_name
                        print(city)
            except Exception as e:
                pass

        state = g.state
        zip_code = g.postal

        try:
            fm_county = g.county.rsplit(' ', 1)[0]
        except Exception as e:
            fm_county = g.county
        # if fm_county == "St":
        #     results = g.content['results'][0]['address_components']
        #     for r in results:
        #         name = r['long_name']
        #         if "County" in name:
        #             fm_county = name.split(" ")[0]
        #             print(fm_county)

        try:
            fm_web = detail_soup.find("a", class_="website--link").attrs["href"]
        except Exception as e:
            # print(e)
            fm_web = ""

        csv_row = [fm_name,
                   fm_description,
                   fm_contact_email,
                   fm_web,
                   fm_county,
                   fm_addr,
                   street,
                   city,
                   state,
                   zip_code,
                   fm_phone,
                   season,
                   fm_lat,
                   fm_long,
                   file_name]

        writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(csv_row)


end_time = datetime.datetime.now()
print(end_time)
total_time = end_time - start_time
print(total_time)
