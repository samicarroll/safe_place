import datetime
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

timestamp = datetime.datetime.now().strftime('%m_%d_%y %H%M%S')
LIST = []
url = 'https://fortmyers.craigslist.org/'
driver = webdriver.Chrome()
driver.get(url)

# CLICK HOUSING WANTED SECTION ON CRAIGSLIST
click = driver.find_element(By.XPATH, '//*[@id="hhh0"]/li[3]/a/span')
driver.execute_script("arguments[0].click();", click)
driver.implicitly_wait(10)

# SEARCH KEYWORD
keyword = driver.find_element(By.XPATH, '/html/body/div[1]/main/form/div[1]/div/div/input')
keyword.send_keys('woman')
keyword.send_keys(Keys.ENTER)

# NUMBER OF SEARCH RESULTS
# results = driver.find_element(By.XPATH, '//*[@id="search-results-page-1"]/ol/div')
# LISTINGS
listings = driver.find_elements(By.CLASS_NAME, 'gallery-card')
for listing in listings:
    title = listing.find_element(By.CLASS_NAME, 'titlestring').text
    print(title)

    meta = listing.find_element(By.CSS_SELECTOR, '.meta').text
    print(meta)

    # FIXME: URL NOT PRINTING
    url = listing.find_element(By.CSS_SELECTOR, '.cl-gallery a').text
    print(url)

    # TODO: FIND DESCRIPTIONS
    # TODO: GET SCREENSHOT FOR EACH LISTING
    #  - POSSIBLY USE BEAUTIFUL SOUP WHEN URL IS OBTAINED
    driver.get_screenshot_as_file(f"megapersonals({timestamp}).png")

    LIST.append([title, meta, url])
    time.sleep(1)

# EXPORT TO EXCEL FILE
columns = ('title', 'meta', 'url')
df = pd.DataFrame(LIST, columns=columns)

df.to_excel(f'craigslist({timestamp}).xlsx', index=False)
print(f'craigslist({timestamp}).xlsx exported.')
# CLOSE WEBDRIVER
driver.close()
