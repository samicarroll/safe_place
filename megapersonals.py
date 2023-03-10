import datetime
import time
import pandas as pd

from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By

# SET UP LIST AND MEGAPERSONALS URL
LIST = []
url = 'https://megapersonals.eu/'

# SET UP HEADLESS PAGE
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

# CONNECT SELENIUM TO WEB URL
driver.get(url)

# DATE FORMAT: MONTH_DAY_YEAR - HOUR_MINUTES_SECONDS
timestamps = datetime.datetime.now().strftime('%m_%d_%y %H_%M_%S')

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

# CLICKING AGREEMENTS AND PREFERENCES:
# CLICK AGE AGREEMENT BUTTON
click = driver.find_element("id", 'ageagree')
driver.execute_script("arguments[0].click();", click)
time.sleep(5)

# CLICK UNITED STATES
us = driver.find_element("id", "ac-United States")
driver.execute_script("arguments[0].click();", us)
time.sleep(5)

# CLICK FLORIDA
fl = driver.find_element("id", "ac-Florida")
driver.execute_script("arguments[0].click();", fl)
time.sleep(5)

# CLICK FORT MYERS
fort_myers = driver.find_element(By.XPATH, '//*[@id="choseCityContainer"]/div[3]/article/div[10]/article/p[3]/a')
driver.execute_script("arguments[0].click();", fort_myers)
time.sleep(5)

# CLICK WOMEN SEARCHING MALE
women_seeking_male = driver.find_element(By.XPATH, '//*[@id="megapCategoriesOrangeButton"]/a')
driver.execute_script("arguments[0].click();", women_seeking_male)
time.sleep(5)

# LOOP THROUGH LISTINGS AND PULL DESIRED INFORMATION
listings = driver.find_elements(By.CLASS_NAME, 'listadd')

# HOLDS LINKS
links = []
container = driver.find_elements(By.ID, "list")
# PULLS URLS FROM EACH LISTING
# FIXME: FOR LOOP DOES NOT ACCESS NESTED FOR LOOP ON PAGE 2
# GRABS 33 URLS FROM PAGE ONE, GOES TO PAGE 2 AND BEGINS GRABBING
# INFORMATION FROM URLS IN LIST RATHER THAN THE URLS ON PAGE 2.
for ads in container:
    for listing in listings:
        # BYPASS STALE ELEMENT
        try:
            urls = listing.find_element(By.TAG_NAME, 'a').get_attribute('href')
        except StaleElementReferenceException:
            pass
        # SAVES URLS TO LIST "LINKS" - DECLARED ON LINE 76
        links.append(urls)
        time.sleep(2)
    # CLICK THE NEXT PAGE - GOES THROUGH FOR LOOP TO GRAB LINKS ON ALL PAGES
    next_page = driver.find_element("id", "paginationNext")
    driver.execute_script("arguments[0].click();", next_page)

# COUNTS THROUGH URLS IN LIST
counter = 0

for urls in links:
    # SETS COUNTER TO LINKS
    driver.get(links[counter])
    # INCREMENTS COUNTER AFTER APPENDS INFO FROM AD
    counter += 1

    # GRAB AD DESCRIPTION
    description = driver.find_element(By.CLASS_NAME, 'postbody').text
    time.sleep(2)
    # CHECKS IF KEYWORD IS IN DESCRIPTION - IF KEYWORD IS PRESENT, APPENDS DATA
    for keyword in keywords:
        if keyword in description:
            page_url = driver.current_url
            time.sleep(2)

            title = driver.find_element(By.CLASS_NAME, 'post_preview_title').text
            time.sleep(2)

            description = driver.find_element(By.CLASS_NAME, 'postbody').text
            time.sleep(2)

            age = driver.find_element(By.CLASS_NAME, 'post_preview_age').text
            time.sleep(2)

            phone_number = driver.find_element(By.CSS_SELECTOR,
                                               'body > div > div.post_preview_body > div.fromLeft.post_preview_phone > span > a').get_attribute(
                "innerHTML")
            time.sleep(2)

            # APPEND CONTENTS TO LIST
            LIST.append([title, age, description, phone_number])

            # SCREENSHOT LISTING
            screenshot_name = f"megapersonals_{counter}_keyword_{keyword.replace(' ', '_')}.png"
            driver.save_screenshot(screenshot_name)

        # SET SCREENSHOT SIZE
        S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
        driver.set_window_size(S('Width'), S('Height'))

# SET UP COLUMNS FOR EXCEL FILE
columns = ('title', 'age', 'description', 'phone number')
df = pd.DataFrame(LIST, columns=columns)

# EXPORT TO EXCEL FILE
df.to_excel(f'megapersonals({timestamps}).xlsx', index=False)
print(f'megapersonals({timestamps}).xlsx exported.')

# CLOSE WEBDRIVER
driver.close()
