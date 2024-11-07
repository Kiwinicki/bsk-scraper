import json
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

service = Service('/usr/local/bin/geckodriver')  # Adjust this path if necessary
driver = webdriver.Firefox(service=service)

driver.get("https://frog02-20741.wykr.es")
product_lists = driver.find_elements(By.CLASS_NAME, "product-list")

data = {}

# TODO: 
# - click button 'Show more' in each category and scrape that
# - make searchbar more advanced (add category list) and scrape category list from searchbar?
# - headless mode?


for product_list in product_lists:
    category = product_list.get_attribute('data-category')
    products = product_list.find_elements(By.CLASS_NAME, 'product-item')
    data[category] = [{
            'name': prod.find_element(By.TAG_NAME, 'h3').text, 
            'price': float(prod.find_element(By.TAG_NAME, 'p').text.split(' ')[0]) 
        } for prod in products]

with open("data.json", "w") as file:
    json.dump(data, file, indent=4)

driver.quit()