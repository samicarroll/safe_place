import datetime
import time
import pandas as pd
import pathlib
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By


def run(selected_keywords):
    # SET UP LIST AND MEGAPERSONALS URL
    LIST = []
    url = 'https://megapersonals.eu/'
    driver = webdriver.Chrome()
    # CONNECT SELENIUM TO WEB URL

    # SET UP HEADLESS PAGE
    options = webdriver.ChromeOptions()
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    chromedriver_binary = "/Users/samicarroll/Documents/drivers/chromedriver_mac64-2/chromedriver"
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(executable_path=chromedriver_binary, chrome_options=options)
    driver.get(url)

    # DATE FORMAT: MONTH_DAY_YEAR - HOUR_MINUTES_SECONDS
    timestamps = datetime.datetime.now().strftime('%m_%d_%y %H_%M_%S')

    # CLICKING AGREEMENTS AND PREFERENCES:
    # CLICK AGE AGREEMENT BUTTON
    time.sleep(5)
    click = driver.find_element(By.CSS_SELECTOR, "#ageagree")
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

    # PULLS URLS FROM EACH LISTING
    pageCounter = 0
    links = []

    while pageCounter <= 4:
        listings = driver.find_elements(By.CLASS_NAME, 'listadd')

        for listing in listings:
            try:
                link = listing.find_element(By.TAG_NAME, 'a').get_attribute('href')
                links.append(link)
            except StaleElementReferenceException:
                continue

        # CLICK THE NEXT PAGE - GOES THROUGH FOR LOOP TO GRAB LINKS ON ALL PAGES
        if pageCounter < 4:
            next_page = driver.find_element("id", "paginationNext")
            driver.execute_script("arguments[0].click();", next_page)
            time.sleep(2)

        pageCounter += 1

    link_counter = 0

    for link in links:
        print(f"Processing link {link_counter + 1}: {link}")  # Debugging print statement
        driver.get(link)

        for keyword in selected_keywords:
            description = driver.find_element(By.CSS_SELECTOR, 'body > div > div.post_preview_body > span').text
            if keyword in description.lower():
                page_url = driver.current_url
                time.sleep(2)

                title = driver.find_element(By.CLASS_NAME, 'post_preview_title').text
                time.sleep(2)

                description = driver.find_element(By.CLASS_NAME, 'postbody').text
                time.sleep(2)

                age = driver.find_element(By.CLASS_NAME, 'post_preview_age').text
                time.sleep(2)

                phone_number = driver.find_element(By.CSS_SELECTOR,
                                                   'body > div > div.post_preview_body > '
                                                   'div.fromLeft.post_preview_phone'
                                                   '> span > a').get_attribute(
                    "innerHTML")
                time.sleep(1)

                # APPEND CONTENTS TO LIST
                LIST.append([link_counter + 1, page_url, title, age, description, phone_number, keyword])

                # SET SCREENSHOT SIZE
                S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
                driver.set_window_size(S('Width'), S('Height'))

                # SCREENSHOT LISTING
                screenshot_name = f"({link_counter + 1})_{timestamps}_megapersonals.png"
                driver.save_screenshot(pathlib.Path.home() / f"Desktop/megapersonals/screenshots/{screenshot_name}")

                break

        link_counter += 1

    # SET UP COLUMNS FOR EXCEL FILE
    columns = ('counter', 'url', 'title', 'age', 'description', 'phone number', 'matching keyword')
    df = pd.DataFrame(LIST, columns=columns)

    # EXPORT TO EXCEL FILE
    df.to_excel(pathlib.Path.home() / f"Desktop/megapersonals/excel_files/megapersonals({timestamps}).xlsx",
                index=False)
    print(f'megapersonals({timestamps}).xlsx exported.')

    # CLOSE WEBDRIVER
    driver.close()
