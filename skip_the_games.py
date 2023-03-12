import datetime
import time

import undetected_chromedriver
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#creates time and date for the screenshot
timestamps = datetime.datetime.now().strftime('%m_%d_%y %H%M%S')
url = 'https://skipthegames.com/'
driver = undetected_chromedriver.Chrome()
driver.get(url)
LIST = []

# WAIT FOR ELEMENTS TO BE CLICKABLE
wait = WebDriverWait(driver, 30)

# ACCEPT COOKIES
cookie = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'cc-cookie-accept')))
cookie.click()

# SELECT PREFERENCES
# WAIT FOR PAGE TO FULLY LOAD
wait.until(EC.element_to_be_clickable((By.NAME, 'input_search_client')))
# SELF-IDENTIFICATION (MALE, WOMAN, ETC.)
identification = Select(driver.find_element(By.NAME, 'input_search_client'))
identification.select_by_value('men')

# LOOKING FOR: ESCORT,
category = Select(wait.until(EC.element_to_be_clickable((By.NAME, 'input_search_category'))))
category.select_by_value('ts-escorts')

# ENTERING FORT MYERS IN CITY TODO: page refresh before able to insert the location
# IT auto-completes and then it can be clicked
#location = wait.until(EC.element_to_be_clickable((By.ID, 'input_search_location')))
#driver.execute_script("arguments[0].value = 'Fort Myers, FL'", location)
location = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'input_text.txt1.ui-autocomplete-input')))
driver.execute_script("arguments[0].value = 'Fort Myers, FL';", location)

# ENTER KEYWORDS
keywords = wait.until(EC.element_to_be_clickable((By.NAME, 'input_search_optional_keywords')))
driver.execute_script("arguments[0].value = 'blonde';", keywords)

# SEARCH
wait.until(EC.element_to_be_clickable((By.ID, 'search_button'))).click()
#location.send_keys(Keys.ENTER)  # search location

wait.until(EC.element_to_be_clickable((By.ID, 'search_button'))).click()

gallery = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.clsfds-display-mode.gallery')))
for ads in gallery:
    posts = ads.find_elements(By.CSS_SELECTOR, '.day-gallery')
    for post in posts:
        date = post.find_element(By.CLASS_NAME, 'post-timestamp').get_attribute('innerHTML')
        print(date)

        title = post.find_element(By.CLASS_NAME, 'post-title').get_attribute('innerHTML')
        print(title)

        description = post.find_element(By.ID, 'post-body').get_attribute('innerHTML')
        print(description)

        age = post.find_element(By.CLASS_NAME, 'ad_display_h3_age').get_attribute('innerHTML')
        print(age)
        #screenshot
        driver.get_screenshot_as_file(f"skipthegames({timestamps}).png")

driver.close()

