from bs4 import BeautifulSoup
import requests
import base64
import logging as Logger


# ------------------- Logging Setup -------------------

Logger.basicConfig(
    level=Logger.INFO,
    format="[%(levelname)s] (%(asctime)s) -> %(message)s",
    handlers=[
        Logger.StreamHandler(),
    ],
)


# --------------------- Constants ---------------------


BASE_URL = "https://www.wsupercars.com/wallpapers/"
BRANDS = [
    "lamborghini",
    "audi",
    "porsche",
    "bmw",
    "mercedes-benz",
]


# --------------------- Utils ---------------------


def gen_id(link: str) -> str:
    """
    Generates a base64 encoded id for the link

    Args:
        link (str): URL of the page

    Returns:
        str: base64 encoded string
    """
    bytes = link.encode("utf-8")
    encoded_data = base64.b64encode(bytes)

    return encoded_data


# --------------------- Script ---------------------


# List of url's to scrape from
car_links = []

# fetch all the car links for each brand
for brand in BRANDS:
    url = f"{BASE_URL}/{brand}/"
    base_page_data = requests.get(url, timeout=30)
    base_soup = BeautifulSoup(base_page_data.content, "html.parser")

    # extract all the links in the page
    lists = base_soup.find_all("ul", class_=["car-list"])

    for item in lists:
        a_tags = item.find_all("a")

        for a in a_tags:
            car_links.append(a["href"])

Logger.info(f"Fetched {len(car_links)} car links")

# scrape `desc` and `car-specs` for each link in [car_links]
for id, link in enumerate(car_links):
    base_page_data = requests.get(link, timeout=30)
    base_soup = BeautifulSoup(base_page_data.content, "html.parser")

    desc = base_soup.find("div", class_=["description"])

    if desc:
        desc = (desc.text).lower()
    else:
        desc = ""

    specs = base_soup.find("ul", class_=["car-specs"])

    if specs:
        specs = (specs.text).lower()
    else:
        specs = ""

    doc_id = gen_id(link)

    with open(f"./cars/{doc_id}.txt", "w") as file:
        file.write(desc)
        file.write("\n")
        file.write(specs)

        file.flush()
