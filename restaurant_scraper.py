from time import sleep
from requests import get
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re

URL = "https://tinyurl.com/552ebk3y"

def get_restaurant_info(index: int, driver):
    name = driver.find_elements_by_class_name("dbg0pd")[index].text
    rating = driver.find_elements_by_xpath("//span[contains(@class, 'BTtC6e')]")[index].text
    description = driver.find_elements_by_class_name("rllt__wrapped")[index].text
    return name, rating, description

def get_miscellaneous(index: int, driver):
    driver.find_elements_by_class_name("dbg0pd")[index].click()
    sleep(3)
    num_reviews = driver.find_elements_by_class_name("Ob2kfd")[0].text.splitlines()[1]
    # uses the split_on_letter function to find the cost (which is a set of $ - nonalphanumeric) and the restaurant_type (which are letters)
    cost = split_on_letter(driver.find_elements_by_class_name("TLYLSe")[1].text)[0]
    restaurant_type = split_on_letter(driver.find_elements_by_class_name("TLYLSe")[1].text)[1]
    # inexpensive ($), moderately priced ($$), or expensive ($$$)
    if cost == "$":
        price = "inexpensive"
    elif cost == "$$":
        price = "moderately priced"
    elif cost == "$$$":
        price = "expensive"    
    return num_reviews, price, restaurant_type
    
def get_reviews(index: int, driver):
    driver.find_elements_by_class_name("dbg0pd")[index].click()
    sleep(3)
    restaurant_reviews = []
    for review_index in range(3):
        review = driver.find_elements_by_class_name("b4vunb")[review_index]
        restaurant_reviews.append(review)
    return restaurant_reviews    

def get_restaurant_images_urls(index: int, driver):
    driver.find_elements_by_class_name("dbg0pd")[index].click()
    sleep(3)
    restaurant_images = []
    for image_index in range(6):
        image = driver.find_elements_by_class_name("vwrQge")[image_index].get_attribute("style")
        # format the image url correctly
        image_url = replace_all(image, {'background-image: url(': '', ');': ''})
        restaurant_images.append(image_url)
    return restaurant_images    

# helper methods

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def split_on_letter(s):
    match = re.compile("[^\W\d]").search(s)
    return [s[:match.start()], s[match.start():]]

if __name__ == "__main__":
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(URL)