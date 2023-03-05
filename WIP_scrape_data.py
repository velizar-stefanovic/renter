from bs4 import BeautifulSoup
import requests
import re
import time
import datetime


def translate_to_utf(word):
    """
    This function translates all Serbian characters
    to corresponding English characters for the
    provided string, due to the issues with storing
    data in CSV files.

    Args:
        word: a string that is being 'translated'

    Returns:
        a string with 'translated' characters

    """

    dict = {
        "Č": "C",
        "Ć": "C",
        "Ž": "Z",
        "Š": "S",
        "Đ": "Dj",
        "č": "c",
        "ć": "c",
        "ž": "z",
        "đ": "dj",
        "š": "s",
    }

    return word.translate(str.maketrans(dict))


def fetch_property_data(list_of_urls):
    """
    This functions scrapes the property data from the
    provided urls, and stores it in the CSV file in
    property-data-fetch S3 bucket.
    """

    now = datetime.datetime.today()
    print(datetime.date(now.year, now.month, now.day))
    count = 0
    fetched_data = []

    for url in list_of_urls:
        page = requests.get(url)
        property = BeautifulSoup(page.content, "html.parser")
        id_property = url[-12:-1]

        property_name = property.find(
            "h1", class_="detail-title pt-3 pb-2"
        ).text.strip()

        dates = property.find("div", class_="updated").text.strip()
        date_post = re.findall("\S*Objavljen: (\S+)", dates)[0]
        date_update = re.findall("\S*Ažuriran: (\S+)\nObjavljen", dates)[0]
        area_m2 = property.find("h4", class_="stickyBox__size").text[:-3]

        price_eur = re.findall(
            "(.*) EUR", property.find("h4", class_="stickyBox__price").text
        )[0].replace(" ", "")

        # sometimes the number of rooms is not provided
        try:
            rooms = float(
                re.findall(
                    ":(\S*)",
                    property.find("div", class_="property__main-details")
                    .find_all("span")[2]
                    .text,
                )[0]
            )
        except:
            rooms = "could not find"

        heating = re.findall(
            ":(\S+)",
            property.find("div", class_="property__main-details")
            .find_all("span")[4]
            .text,
        )[0]

        parking = re.findall(
            ":(\S+)",
            property.find("div", class_="property__main-details")
            .find_all("span")[6]
            .text,
        )[0]

        furniture = re.findall(
            ":(.+)",
            property.find("div", class_="property__main-details")
            .find_all("span")[10]
            .text,
        )[0]

        details = " ".join(
            property.find("div", class_="property__amenities").text.split()
        )

        # sometimes, the description could be shown in different places, or is not provided at all
        try:
            description = (
                (property.find("div", class_="cms-content-inner").find_all("p")[2].text)
                .strip()
                .replace("\n", " ")
                .replace("\r", " ")
            )
        except:
            try:
                description = (
                    property.find("div", class_="cms-content-inner")
                    .text.strip()
                    .replace("\n", " ")
                    .replace("\r", " ")
                )
            except:
                description = "could not find"
        location = ", ".join(
            property.find("div", class_="property__location").text.strip().split("\n")
        )

        my_object = {
            "id_property": id_property,
            "date_scrape": datetime.date(now.year, now.month, now.day),
            "property_name": translate_to_utf(property_name),
            "date_post": date_post,
            "date_update": date_update,
            "area_m2": area_m2,
            "price_eur": price_eur,
            "rooms": rooms,
            "heating": translate_to_utf(heating),
            "parking": parking,
            "furniture": translate_to_utf(furniture),
            "details": translate_to_utf(details),
            "description": translate_to_utf(description),
            "location": translate_to_utf(location),
        }

        fetched_data.append(my_object)

        print(f"Property number {list_of_urls.index(url)+1} is scraped: {id_property}")
        count += 1

        # pause scraping every 10 pages
        if count % 10 == 0 and count != len(list_of_urls):
            print("Pausing for a bit...")
            time.sleep(2)

    return fetched_data
