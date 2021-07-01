from time import sleep
from requests import get
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import re
import os

URL = "https://tinyurl.com/552ebk3y"

def get_restaurant_name_and_rating(index: int, driver):
    name = driver.find_elements_by_class_name("dbg0pd")[index].text
    rating = driver.find_elements_by_xpath("//span[contains(@class, 'BTtC6e')]")[index].text + " / 5.0"   
    return name, rating

def get_miscellaneous(index: int, driver):
    driver.find_elements_by_class_name("dbg0pd")[index].click()
    sleep(3)
    num_reviews = driver.find_elements_by_class_name("Ob2kfd")[0].text.splitlines()[1]
    reviews = get_reviews(driver)
    image_urls = get_restaurant_images_urls(driver)
    # uses the split_on_letter function to find the cost (which is a set of $ - nonalphanumeric) and the restaurant_type (which are letters)
    cost = split_on_letter(driver.find_elements_by_class_name("TLYLSe")[1].text)[0]
    restaurant_type = split_on_letter(driver.find_elements_by_class_name("TLYLSe")[1].text)[1]
    if cost == "$":
        price = "Inexpensive"
    elif cost == "$$":
        price = "Moderately priced"
    elif cost == "$$$":
        price = "Expensive"
    else:
        price = "Not found"    
    service_options = get_line_with_word("Service", driver)
    address = get_line_with_word("Address", driver)
    menu = get_line_with_word("Menu", driver)
    phone_number = get_line_with_word("Phone", driver)        
    return num_reviews, reviews, image_urls, price, restaurant_type, service_options, address, menu, phone_number
    
def get_reviews(driver):
    restaurant_reviews = []
    for review_index in range(3):
        review = driver.find_elements_by_class_name("b4vunb")[review_index].text
        restaurant_reviews.append(review)
    return restaurant_reviews    

def get_restaurant_images_urls(driver):
    restaurant_images = []
    for image_index in range(6):
        image = driver.find_elements_by_class_name("vwrQge")[image_index].get_attribute("style")
        # format the image url correctly
        image_url = replace_all(image, {'background-image: url(\"': '', '\");': ''})
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

# gets lines in the pop out screen for info such as service options, address, etc.
def get_line_with_word(word: str, driver):
    lines = driver.find_elements_by_class_name("ifM9O")[0].text.split("\n")
    # iterate over lines, and print out line numbers which contain the word of interest.
    for i, line in enumerate(lines):
        if word in line:
            return driver.find_elements_by_class_name("ifM9O")[0].text.splitlines()[i]

if __name__ == "__main__":
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(URL)

    for restaurant_index in range(1):
        name, rating = get_restaurant_name_and_rating(restaurant_index, driver)
        num_reviews, reviews, image_urls, price, restaurant_type, service_options, address, menu, phone_number = get_miscellaneous(restaurant_index, driver)
        restaurant_num = restaurant_index + 1
        folder_name = "{}. {}".format(restaurant_num, name)
        os.makedirs(folder_name, exist_ok=True)
        restaurant_details = f'{folder_name}/Restaurant Details'
        restaurant_info = ("Rating: " + rating + "\nNumber of Reviews: " + num_reviews + "\nA few reviews:\n" + ",\n".join(reviews) + 
        "\nCost: " + price + "\nType of restaurant: " + restaurant_type + "\n" + service_options + "\n" + address + "\n" + menu + "\n" + phone_number)
        with open(restaurant_details, "w") as restaurant_details_file:
            restaurant_details_file.write(restaurant_info)
        for i in range(len(image_urls)):
            # I was using Image.open() and then image.show() with the Pillow imaging library but it just spams computer with image files
            # image = Image.open(get(image_urls[i], stream=True).raw)
            # image.show()
            restaurant_images = f'{folder_name}/Restaurant Image {i + 1}'
            with open(restaurant_images, "wb") as restaurant_images_file:
                restaurant_images_file.write(get(image_urls[i]).content)