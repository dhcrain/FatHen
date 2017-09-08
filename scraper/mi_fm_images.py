import unicodedata
import requests
from bs4 import BeautifulSoup
import geocoder
import csv
import datetime
import re
from io import open as iopen
# from urlparse import urlsplit
from urllib.parse import urlsplit
from pathlib import Path

start_time = datetime.datetime.now()
print(start_time)


def requests_image(file_url, file_name):
    suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg', ]
    # file_name = urlsplit(file_url)[2].split('/')[-1]
    # path = Path('/mi_images/' + file_name)
    # path.parent.mkdir(parents=True, exist_ok=True)

    file_suffix = file_name.split('.')[1]
    i = requests.get(file_url)
    if file_suffix in suffix_list and i.status_code == requests.codes.ok:
        with iopen(file_name, 'wb') as file:
            file.write(i.content)
    else:
        return False

page_size = 5
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
    if img_link is not None:
        img_url = 'http:' + img_link.attrs['src'].replace('ar_5:4,c_fill,w_200,g_face,q_50/', '')
        file_name = fm_name.replace(' ', '_').replace(',', '').replace("'", "").lower() + '.jpg'
        print(file_name)
        print(img_url)
        requests_image(img_url, file_name)


end_time = datetime.datetime.now()
print(end_time)
total_time = end_time - start_time
print(total_time)
