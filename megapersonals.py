import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# SET UP LIST AND WEBDRIVER - CONNECT SELENIUM TO WEB URL
LIST = []
url = 'https://megapersonals.eu/public/post_list/234/1/1/meetup'
driver = webdriver.Chrome()
driver.get(url)
timestamp = datetime.datetime.now().strftime('%m_%d_%y %H%M%S')


# CLICKING AGREEMENTS AND PREFERENCES:
# CLICK AGE AGREEMENT BUTTON
click = driver.find_element("id", 'ageagree')
driver.execute_script("arguments[0].click();", click)
print("page title is:", driver.title)
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
driver.implicitly_wait(5)


# LOOP THROUGH LISTINGS AND PULL DESIRED INFORMATION
listings = driver.find_elements(By.CLASS_NAME, 'listadd')

for listing in listings:
    post_time = listing.find_element(By.CLASS_NAME, 'gallerylistdate1').text

    # TODO: DEBUG REPEATING TITLE ENTRIES
    # FIXME: DUPLICATE TITLE ENTRIES
    # XPATH MAY NOT BE EFFICIENT - XPATH UNIQUE TO POST
    title = listing.find_element(By.XPATH, '//*[@id="list"]/div[2]/div[3]/a')

    age = listing.find_element(By.CLASS_NAME, 'titleAge').text

    description = listing.find_element(By.CLASS_NAME, 'listbody').text

    # TODO: DEBUG URL NOT EXPORTING
    # FIXME: URL NOT EXPORTING
    # XPATH MAY NOT BE EFFICIENT FOR PULLING - XPATH UNIQUE TO POST
    listing_url = listing.find_element(By.XPATH, '//*[@id="list"]/div[2]/div[3]/a').text
    print(listing_url)

    driver.get_screenshot_as_file(f"megapersonals({timestamp}).png")
    # phone_number = listing.find_element(By.XPATH, './html/body/div/div[6]/div[1]/span/a').text
    # page numbers - /html/body/div/div[7]/div/div/div[6]/a ; /html/body/div/div[7]/div/div/div[6]/a ; class = pageNumbersNew

    # APPEND THE DICTIONARY CONTENTS TO LIST
    LIST.append([post_time, title, age, description])
    time.sleep(1)

# EXPORT TO EXCEL FILE
columns = ('time', 'title', 'age', 'description')
df = pd.DataFrame(LIST, columns=columns)

df.to_excel(f'megapersonals({timestamp}).xlsx', index=False)
print(f'megapersonals({timestamp}).xlsx exported.')
# CLOSE WEBDRIVER
driver.close()
