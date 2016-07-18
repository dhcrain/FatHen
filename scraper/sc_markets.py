import requests
from bs4 import BeautifulSoup
import geocoder
import csv

with open ("sc_farmers_markets.csv", "w", newline="") as outfile:

    url = "https://agriculture.sc.gov/where-to-buy-local/community-based-farmers-markets/"
    content = requests.get(url).text
    souper = BeautifulSoup(content, "html.parser")
    results = souper.find_all("a", class_="link-wrapper")

    # print(results)

    for result in results:
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
            if "Contact:" in item.text:
                contact_name = item.text.split(":")[1].strip()
            elif "Email:" in item.text:
                contact_email = item.text.split(":")[1].strip()
            elif "Facility Type:" in item.text:
                facility_type = item.text.split(":")[1].strip()
            elif "County:" in item.text:
                mrkt_county = item.text.split(":")[1].strip()
                print([mrkt_county])

            elif "Address" in item.text:
                mrkt_address = item.text.split(":")[1].strip()
                g = geocoder.google(mrkt_address)
                mrkt_addr = g.address

            # elif "Mailing" in item.text:
            #     mrkt_mailing_address = item.text.split(":")[1]
            #     print(mrkt_mailing_address)
                # gm = geocoder.google(mrkt_mailing_address)
                # mrkt_mail_addr = gm.address
                # print(gm.address)

            elif "Programs Accepted:" in item.text:
                programs_accepted = item.text.split(":")[1].strip()
            elif "Phone:" in item.text:
                mrkt_phone = item.text.split(":")[1]
            elif "Hours of Operation:" in item.text:
                hrs_of_operation = item.text.split(":")[1].strip()
            elif "Seasons of Operation:" in item.text:
                seasons_of_operation = item.text.split(":")[1].strip()

            try:
                if "Is Handicap Accessible?" in item.text:
                    handicap_accessible = item.text.split(":")[1].strip()
            except IndexError:
                handicap_accessible = ""

            market_iframe = market_souper.find("iframe")
            try:
                market_iframe_url = market_iframe.attrs['src']
            except AttributeError:
                market_iframe_url = ""

        # print(market_name, contact_name, contact_email, facility_type, mrkt_county, mrkt_addr, programs_accepted, mrkt_phone, hrs_of_operation, seasons_of_operation, handicap_accessible, market_iframe_url)

        csv_row = [market_name, contact_name, contact_email, facility_type, mrkt_county, mrkt_addr, programs_accepted, mrkt_phone, hrs_of_operation, seasons_of_operation, handicap_accessible, market_iframe_url]

        writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(csv_row)
