import datetime
import time
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
import pandas as pd

from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# SET UP LIST AND WEBDRIVER - CONNECT SELENIUM TO WEB URL
LIST = []
url = 'https://megapersonals.eu/'

# SET UP HEADLESS PAGE
# options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()  # TODO: USED IN TESTING - DELETE BEFORE DEPLOYMENT
driver.get(url)
timestamps = datetime.datetime.now().strftime('%m_%d_%y %H%M%S')

# LIST FOR KEYWORDS
keywords = [
    "no cops",
    "woman",
    "escort",
    "young",
    "phone number",
    "no police",
    "police",
    "cops",
    "law enforcement",
    "discreet location",
    "snap chat",
    "snapchat",
    "e$cort",
]

# WAIT FOR ELEMENTS
wait = WebDriverWait(driver, 10)
# CLICKING AGREEMENTS AND PREFERENCES:
# CLICK AGE AGREEMENT BUTTON
click = driver.find_element("id", 'ageagree')
driver.execute_script("arguments[0].click();", click)
print("page title is:", driver.title)  # TODO: TEST PRINT - REMOVE BEFORE DEPLOYMENT
driver.implicitly_wait(5)

# CLICK UNITED STATES
us = driver.find_element("id", "ac-United States")
driver.execute_script("arguments[0].click();", us)
driver.implicitly_wait(5)

# CLICK FLORIDA
fl = driver.find_element("id", "ac-Florida")
driver.execute_script("arguments[0].click();", fl)
driver.implicitly_wait(5)

# CLICK FORT MYERS
fort_myers = driver.find_element(By.XPATH, '//*[@id="choseCityContainer"]/div[3]/article/div[10]/article/p[3]/a')
driver.execute_script("arguments[0].click();", fort_myers)
driver.implicitly_wait(5)
# CLICK WOMEN SEARCHING MALE
women_seeking_male = driver.find_element(By.XPATH, '//*[@id="megapCategoriesOrangeButton"]/a')
driver.execute_script("arguments[0].click();", women_seeking_male)
time.sleep(5)

# LOOP THROUGH LISTINGS AND PULL DESIRED INFORMATION
# container = driver.find_elements(By.ID, 'list')
# for posts in container:

# HOLDS LINKS
listings = driver.find_elements(By.CLASS_NAME, 'listadd')
# ENTERS EACH LISTING TO PULL INFORMATION
# for post in listings:
links = []
for listing in listings:
    # BYPASS STALE ELEMENT
    try:
        urls = listing.find_element(By.TAG_NAME, 'a').get_attribute('href')
    except StaleElementReferenceException:
        pass
    # counter = 0
    # FIXME: ONLY GRABBING THE FIRST LINK
    links.append(urls)

counter = 0
for urls in links:
    driver.get(links[counter])
    counter += 1
    # check if keyword is in the page source and takes screenshot with the keyword found
    for keyword in keywords:
        if keyword in driver.page_source:
            print(links)  # TODO: TEST PRINT REMOVE BEFORE DEPLOYMENT
            screenshot_name = f"megapersonals_{counter}_keyword_{keyword.replace(' ', '_')}.png"
            driver.save_screenshot(screenshot_name)

        # SET SCREENSHOT SIZE
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
    driver.set_window_size(S('Width'), S('Height'))

    # post_time = listing.find_element(By.CLASS_NAME, 'post_preview_date_time').text
    # time.sleep(5)
    # title = wait.until(EC.visibility_of_element_located(By.CLASS_NAME('post_preview_title'))).text
    # time.sleep(5)
    # age = listing.find_element(By.CSS_SELECTOR, 'body > div > div.isee-age > div.post_preview_age').text
    # time.sleep(5)
    # description = listing.find_element(By.CSS_SELECTOR, 'body > div > div.post_preview_body > span').text
    # time.sleep(5)
    # phone_number = listing.find_element(By.CSS_SELECTOR, 'body > div > div.post_preview_body > div.fromLeft.post_preview_phone > span > a').text
    # time.sleep(5)
    # APPEND CONTENTS TO LIST
    # LIST.append([post_time, title, age, description])

# EXPORT TO EXCEL FILE
columns = ('time', 'title', 'age', 'description')
df = pd.DataFrame(LIST, columns=columns)

df.to_excel(f'megapersonals({timestamps}).xlsx', index=False)
print(f'megapersonals({timestamps}).xlsx exported.')
# CLOSE WEBDRIVER
driver.close()
