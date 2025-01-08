import json
import time
import random
import re
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://frog02-20741.wykr.es/'  # https://kamilex106.pl/


class SitemapError(Exception):
    pass


def get_links():
    sitemap_url = BASE_URL + "sitemap.xml"
    response = requests.get(sitemap_url)

    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content, 'xml')
            links = [loc.text for loc in soup.find_all('loc') if loc.text]
            return links
        except Exception as e:
            print(f"Error parsing XML: {e}")
    else:
        raise SitemapError(f"Failed to retrieve the sitemap. Status code: {response.status_code}")


def get_products(link):
    response = requests.get(link)
    if response.status_code != 200:
        print(f"Failed to retrieve link: {link}. Status code: {response.status_code}")
        return {}

    soup = BeautifulSoup(response.content, 'html.parser')
    product_lists = soup.find_all(class_='product-list')

    data = {}
    category_match = re.search(r'[?&]category=([^&]*)', link)
    if not category_match:
        print(f"Category not found in link: {link}")
        return data

    category = category_match.group(1)
    products = []

    for product_list in product_lists:
        product_items = product_list.find_all(class_='product-item')
        for prod in product_items:
            name = prod.find('h3').text.strip() if prod.find('h3') else "Unknown"
            price_text = prod.find('p').text.strip() if prod.find('p') else "0"
            price = float(re.search(r'\d+(\.\d+)?', price_text).group()) if re.search(r'\d+(\.\d+)?', price_text) else 0
            products.append({'name': name, 'price': price})

    data[category] = products
    return data


if __name__ == '__main__':
    try:
        all_data = {}
        links = get_links()
        category_links = [link for link in links if "category" in link]

        for link in category_links:
            all_data.update(get_products(link))
            time.sleep(random.uniform(1, 3))  # Politeness delay to prevent server overload

        with open("data.json", "w") as file:
            json.dump(all_data, file, indent=4)

    except SitemapError as e:
        print(f"Sitemap error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
