from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

LIST = []
url = 'https://fortmyers.craigslist.org/'
driver = webdriver.Chrome()
driver.get(url)

# CLICK HOUSING WANTED SECTION ON CRAIGSLIST
click = driver.find_element(By.XPATH, '//*[@id="hhh0"]/li[3]/a/span')
driver.execute_script("arguments[0].click();", click)
print("page title is:", driver.title)
driver.implicitly_wait(5)
# SEARCH KEYWORD
keyword = driver.find_element(By.XPATH, '/html/body/div[1]/main/form/div[1]/div/div/input')
keyword.send_keys('woman')
keyword.send_keys(Keys.ENTER)
driver.implicitly_wait(5)

# NUMBER OF SEARCH RESULTS
results = driver.find_element(By.XPATH, '//*[@id="search-results-page-1"]/ol/div')
# LISTINGS
listings = driver.find_elements(By.CLASS_NAME, 'results cl-results-page cl-search-view-mode-gallery narrow')
for listing in listings:
    title = listing.find_element(By.CLASS_NAME, 'cl-search-result cl-search-view-mode-gallery').text
    date = listing.find_element(By.XPATH, '/html/head/meta[7]').text
    url = listing.find_element(By.XPATH, '//*[@id="search-results-page-1"]/ol/li[1]/div/a').text
    print(title, date, url)

