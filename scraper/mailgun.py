import requests
from bs4 import BeautifulSoup
import geocoder
import csv
import datetime


url = "https://agriculture.sc.gov/where-to-buy-local/community-based-farmers-markets/"
content = requests.get(url).text
souper = BeautifulSoup(content, "html.parser")
results = souper.find_all("a", class_="link-wrapper")

# print(results)

for result in results:
    fm_web = ""
    market_url = result.attrs['href']
    market_content = requests.get(market_url).text
    market_souper = BeautifulSoup(market_content, "html.parser")
    market_name = market_souper.find(class_="page-title-col").text.strip()
    # can I chunk this out into smaller bits
    market_info = market_souper.find(class_="main-content-col")
    # print(market_info)
    mrkt_info_p = market_info.find_all('p')
    # print(mrkt_info_p)  # list of <p>
    for item in mrkt_info_p:

        if "Address" in item.text:
            mrkt_address = item.text.split(":")[1].strip()
            print(mrkt_address)
            g = geocoder.google(mrkt_address)
            print("housenumber {}, street_number {}, street {}, city {}, state {}, postal {}".format(g.housenumber, g.street_number, g.street, g.city, g.state, g.postal))
            mrkt_addr = g.address
