import datetime
import time
import pandas as pd
import pathlib
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By


def run(selected_keywords):
    LIST = []
    url = 'https://megapersonals.eu/'
    driver = webdriver.Chrome()
    driver.get(url)
    timestamps = datetime.datetime.now().strftime('%m_%d_%y %H_%M_%S')
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
    print(f"Found {len(links)} ads")
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
        print(f"Processing ad {counter + 1}/{len(links)}")
        driver.get(links[counter])
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

                LIST.append([counter, title, age, description, phone_number, keywords])
                screenshot_name = f"megapersonals_{counter}_keyword_{keyword.replace(' ', '_')}.png"
                driver.save_screenshot(screenshot_name)
            S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
            driver.set_window_size(S('Width'), S('Height'))

    # SET UP COLUMNS FOR EXCEL FILE
    columns = ('counter', 'url', 'title', 'age', 'description', 'phone number', 'matching keyword')
    df = pd.DataFrame(LIST, columns=columns)

    # EXPORT TO EXCEL FILE
    df.to_excel(pathlib.Path.home() / f"Desktop/megapersonals/excel_files/megapersonals({timestamps}).xlsx", index=False)
    print(f'megapersonals({timestamps}).xlsx exported.')

    # CLOSE WEBDRIVER
    driver.close()

