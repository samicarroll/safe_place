import datetime
import time

import self as self
# import pandas as pd
import undetected_chromedriver

from selenium.common import StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
timestamps = datetime.datetime.now().strftime('%m_%d_%y %H%M%S')
url = 'https://skipthegames.com/posts/fort-myers'

headers = {
    'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36 Edg/108.0.1462.54'
}
# SET UP HEADLESS PAGE
# options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
# driver = undetected_chromedriver.Chrome(options=options)
driver = undetected_chromedriver.Chrome()
driver.implicitly_wait(60)
driver.get(url)
time.sleep(5)
LIST = []

# WAIT FOR ELEMENTS TO BE CLICKABLE
wait = WebDriverWait(driver, 10)

# LIST FOR KEYWORDS
keywords = [
    "no cops",
    "woman",
    "escort",
    "young",
    "phone number",
    "no police",
    "law enforcement",
    "discreet location",
    "snap chat",
    "snapchat",
    "e$cort",
    "baby"
]

driver.refresh()
# ACCEPT COOKIES
cookie = driver.find_element(By.CLASS_NAME, 'cc-cookie-accept')
driver.execute_script("arguments[0].click();", cookie)
driver.implicitly_wait(10)

# SELECT PREFERENCES
# SELF-IDENTIFICATION (MALE, WOMAN, ETC.)
identification = Select(driver.find_element(By.NAME, 'input_search_client'))
identification.select_by_value('men')
driver.implicitly_wait(10)

# LOOKING FOR: ESCORT,
category = Select(driver.find_element(By.NAME, 'input_search_category'))
category.select_by_value('female-escorts')
driver.implicitly_wait(10)

# ENTER KEYWORDS
# keywords = driver.find_element(By.NAME, 'input_search_optional_keywords')
# keywords.send_keys('blonde')

# # FAST RESULTS
# fast_results = driver.find_element(By.ID, 'radio_clsfd_display_mode_single')
# driver.execute_script("arguments[0].click();", fast_results)
# driver.implicitly_wait(10)

links = []
driver.refresh()
table = driver.find_element(By.ID, 'quick_view')
rows = table.find_elements(By.TAG_NAME, 'tr')
for row in rows:
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'td')))
    columns = row.find_elements(By.TAG_NAME, 'td')
    for column in columns:
        try:
            tag = column.find_element(By.TAG_NAME, 'a').get_attribute('href')
            print(tag)
        except StaleElementReferenceException:
            pass
# for listing in listings:
#     pageLink = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a'))).get_attribute('href')
#     # BYPASS STALE ELEMENT
#     # try:
#     #     pageLink = listing.find_element(By.TAG_NAME, 'a').get_attribute('href')
#     # except StaleElementReferenceException:
#     #     pass
#     # # SAVES URLS TO LIST "LINKS" - DECLARED ON LINE 76
#     # //*[@id="quick_view"]/table/tbody
#     links.append(pageLink)
#     time.sleep(5)
# counter = 0

# for urls in links:
#     # SETS COUNTER TO LINKS
#     driver.get(links[counter])
#     # INCREMENTS COUNTER AFTER APPENDS INFO FROM AD
#     counter += 1
#
#     for keyword in keywords:
#         if keyword in driver.page_source:
#             driver.get_screenshot_as_file(f"skipthegames({timestamps}).png")

# EXPORT TO EXCEL
# columns = ('date', 'title', 'description', 'age')
# df = pd.DataFrame(LIST, columns=columns)
#
# df.to_excel(f'skipthegames({timestamps}).xlsx', index=False)
# print(f'skipthegames({timestamps}).xlsx exported.')
# CLOSE WEBDRIVER
driver.close()
