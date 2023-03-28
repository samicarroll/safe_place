import datetime
import time
import pandas as pd
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By


def run(selected_keywords):
    LIST = []
    url = 'https://megapersonals.eu/'
    driver = webdriver.Chrome()
    driver.get(url)
    timestamps = datetime.datetime.now().strftime('%m_%d_%y %H_%M_%S')

    # Remove the following lines:
    # file = selected_keywords
    # lines = file.read()

    # Replace with:
    keywords = selected_keywords

    click = driver.find_element("id", 'ageagree')
    driver.execute_script("arguments[0].click();", click)
    time.sleep(5)
    us = driver.find_element("id", "ac-United States")
    driver.execute_script("arguments[0].click();", us)
    time.sleep(5)
    fl = driver.find_element("id", "ac-Florida")
    driver.execute_script("arguments[0].click();", fl)
    time.sleep(5)
    fort_myers = driver.find_element(By.XPATH, '//*[@id="choseCityContainer"]/div[3]/article/div[10]/article/p[3]/a')
    driver.execute_script("arguments[0].click();", fort_myers)
    time.sleep(5)
    women_seeking_male = driver.find_element(By.XPATH, '//*[@id="megapCategoriesOrangeButton"]/a')
    driver.execute_script("arguments[0].click();", women_seeking_male)
    time.sleep(5)
    listings = driver.find_elements(By.CLASS_NAME, 'listadd')
    links = []
    pageCounter = 0
    while pageCounter <= 2:
        for listing in listings:
            try:
                urls = listing.find_element(By.TAG_NAME, 'a').get_attribute('href')
            except StaleElementReferenceException:
                pass
            links.append(urls)
            time.sleep(5)
        next_page = driver.find_element("id", "paginationNext")
        driver.execute_script("arguments[0].click();", next_page)
        pageCounter += 1
    counter = 0
    for urls in links:
        driver.get(links[counter])
        counter += 1
        description = driver.find_element(By.CLASS_NAME, 'postbody').text
        time.sleep(2)
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
                LIST.append([title, age, description, phone_number])
                screenshot_name = f"megapersonals_{counter}_keyword_{keyword.replace(' ', '_')}.png"
                driver.save_screenshot(screenshot_name)

        S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
        driver.set_window_size(S('Width'), S('Height'))
    columns = ('title', 'age', 'description', 'phone number')
    df = pd.DataFrame(LIST, columns=columns)

    # EXPORT TO EXCEL FILE
    df.to_excel(f'megapersonals({timestamps}).xlsx', index=False)
    print(f'megapersonals({timestamps}).xlsx exported.')

    # CLOSE WEBDRIVER
    driver.close()
