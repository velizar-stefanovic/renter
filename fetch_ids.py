from bs4 import BeautifulSoup
import requests
import time
import datetime
import boto3
import pandas as pd


def fetch_property_ids(event, context):
    """
    This function goes to the www.nekretnine.rs webpage that
    contains renting properties, fetches the ids of all
    existing properties, and stores them in CSV file in
    property-ids-fetch S3 bucket.

    Args:
        event object: information about the event
        context object:information about the invocation, function
            configuration and execution environment

    Returns:
        status code, number of pages it fetched property ids from,
        number of properties fetched, execution running time.
    """

    start_time = time.time()
    bucket_name = "property-ids-fetch"
    s3 = boto3.client("s3")
    starting_url = "https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/izdavanje/grad/beograd/lista/po-stranici/10/"
    pages = 1000
    page_count = 0
    empty_page = 0
    property_ids = []

    for i in range(1, pages + 1):

        # this solves having the first page URL different then other pages
        if i == 1:
            page = requests.get(starting_url)
        else:
            url = starting_url + f"stranica/{i}/"
            page = requests.get(url)

        soup = BeautifulSoup(page.content, "html.parser")
        all_links = soup.find_all("div", class_="placeholder-preview-box ratio-1-1")

        # this solves the everyday change of the total number of website pages -> break if 3 pages in a row are empty
        if empty_page > 2:
            print("No more data. Breaking...")
            break
        if len(all_links) < 1:
            empty_page += 1
            print("Empty page. Continuing...")
            continue

        # this takes only the property_id part from the URL, which is the last part
        for link in all_links:
            link_words = link.a["href"].split("/")
            # this solves a bug that sometimes happens
            if link_words[-1] == "":
                property_ids.append(link_words[-2])
            else:
                property_ids.append(link_words[-1])

        if len(all_links) > 0:
            page_count += 1

        print(f"Page {i} is done.")

        # pause fetching every 10 pages
        if i % 10 == 0 and i != (pages):
            print("Pausing for a bit...")
            time.sleep(2)

    end_time = time.time()
    running_time = str(datetime.timedelta(seconds=round(end_time - start_time)))
    now = datetime.datetime.today()
    fetching_date = datetime.date(now.year, now.month, now.day)
    url_count = len(property_ids)

    df = pd.DataFrame(property_ids, columns=["property_id"])

    # Convert the DataFrame to a CSV string
    csv_str = df.to_csv(index=False)

    # Encode the CSV string as bytes
    csv_bytes = csv_str.encode()

    # Write the bytes to the S3 bucket
    s3.put_object(
        Bucket=bucket_name, Key=f"nekretnine_{fetching_date}.csv", Body=csv_bytes
    )

    return {
        "statusCode": 200,
        "pageCount": page_count,
        "urlCount": url_count,
        "runningTime": running_time,
    }
