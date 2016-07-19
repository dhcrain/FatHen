import requests
from bs4 import BeautifulSoup
import csv
import datetime
import time

start_time = datetime.datetime.now()
print(start_time)

with open ("gvl_mainst_vendors.csv", "w", newline="") as outfile:

    url = "http://www.saturdaymarketlive.com/101/Current-Vendors"
    content = requests.get(url).text
    souper = BeautifulSoup(content, "html.parser")
    results = souper.find_all("a", class_="Hyperlink")

    for result in results:
        vendor_url = result.attrs['href']
        # print(vendor_url)
        base_url = "http://www.saturdaymarketlive.com"
        if len(vendor_url) <= 4:
            vendor_content = requests.get(base_url + vendor_url).text
        else:
            vendor_content = requests.get(vendor_url).text
        # time.sleep(.5)
        # print(vendor_content)
        vendor_souper = BeautifulSoup(vendor_content, "html.parser")
        # print(vendor_souper)
        vendor_name = vendor_souper.find(id="versionHeadLine").text.strip()
        print(vendor_name)
        vendor_desc = vendor_souper.find(class_="widget editor pageStyles narrow").text.strip()
        # print(vendor_desc)
        vendor_link = vendor_souper.find_all(class_="widgetBody ")
        try:
            if vendor_link[1]:
                try:
                    vendor_web = vendor_link[1].find("a").attrs['href']
                except AttributeError:
                    vendor_web = ""
        except IndexError:
            vendor_web = ""
        print(vendor_web)


        csv_row = [vendor_name, vendor_desc, vendor_web]

        writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(csv_row)


end_time = datetime.datetime.now()
print(end_time)
total_time = end_time - start_time
print(total_time)
