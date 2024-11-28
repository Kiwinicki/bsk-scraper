import json
import time
import random
import re
import requests
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

BASE_URL = 'https://frog02-20741.wykr.es/' # https://kamilex106.com/
HEADLESS = False

class SitemapError(Exception):
    pass

def get_links():
    sitemap_url = "https://frog02-20741.wykr.es/sitemap.xml" #BASE_URL+"sitemap.xml"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
        "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Connection": "keep-alive",
        "Referer": sitemap_url,
        "Sec-Fetch-Dest": "image",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=6",
    }

    response = requests.get(sitemap_url, headers=headers)

    if response.status_code == 200:
        try:
            root = ET.fromstring(response.content)
            links = []
            for url in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
                loc = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
                if loc is not None and loc.text:
                    links.append(loc.text)

            return links

        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
    else:
        raise SitemapError(f"Failed to retrieve the sitemap. Status code: {response.status_code}")


def get_products(driver, link):
    driver.get(link)
    product_lists = driver.find_elements(By.CLASS_NAME, "product-list")

    data = {}
    for product_list in product_lists:
        category = re.search(r'[?&]category=([^&]*)', link).group(1)
        products = product_list.find_elements(By.CLASS_NAME, 'product-item')
        data[category] = [{
                'name': prod.find_element(By.TAG_NAME, 'h3').text, 
                'price': float(prod.find_element(By.TAG_NAME, 'p').text.split(' ')[0]) 
            } for prod in products]
        
        time.sleep(random.uniform(1, 3))
    
    return data


if __name__ == '__main__':
    service = Service('/usr/local/bin/geckodriver')  # Adjust this path if necessary
    options = webdriver.FirefoxOptions()
    if HEADLESS:
        options.add_argument('--headless')
    driver = webdriver.Firefox(service=service, options=options)
    all_data = {}

    links = get_links()
    category_links = [s for s in links if "category" in s]
    for link in category_links:
        all_data.update(get_products(driver, link))

    with open("data.json", "w") as file:
        json.dump(all_data, file, indent=4)

    driver.quit()