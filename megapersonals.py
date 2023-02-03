from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

LIST = []
url = 'https://megapersonals.eu/public/post_list/234/1/1/meetup'
driver = webdriver.Chrome()
driver.get(url)

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
# LISTINGS
listings = driver.find_elements(By.CLASS_NAME, 'listadd')
for listing in listings:
    date = listing.find_element(By.CLASS_NAME, 'gallerylistdate1').text
    print(date)
    title = listing.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/div[3]/div[1]/a').text
    print(title)
    age = listing.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/div[3]/div[1]/div[3]').text
    print(age)
    description = listing.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/div[3]/div[2]').text
    print(description)
    # phone_number = listing.find_element(By.XPATH, './html/body/div/div[6]/div[1]/span/a').text

    dictionary = {
        'Date': date,
        'Title': title,
        'Age': age,
        'Description': description,
        # 'phone_number': phone_number
    }

    LIST.append(dictionary)
df = pd.DataFrame(LIST)
df.to_excel('megapersonals.xlsx')

# SAVE DATA TO EXCEL FILE
columns = ['Date', 'Title', 'Age', 'Description']
df = pd.DataFrame(LIST, columns=columns)
df.to_excel('megapersonals.xlsx')
