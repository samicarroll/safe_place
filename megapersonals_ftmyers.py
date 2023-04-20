import datetime
import pandas as pd
import pathlib
import selenium
import os
import chromedriver_autoinstaller
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By


def run(selected_keywords):
    # SET UP LIST AND MEGAPERSONALS URL
    LIST = []
    url = 'https://megapersonals.eu/'

    # SET UP HEADLESS PAGE
    options = selenium.webdriver.ChromeOptions()
    chromedriver_autoinstaller.install()
    # service_object = Service(binary_path)
    # options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    # chromedriver_binary = "/Users/samicarroll/Documents/drivers/chromedriver_mac64-2/chromedriver"
    options.add_argument("--headless=new")
    options.add_argument("--no-default-browser-check")
    # executable_path=chromedriver_binary, inside next line
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)

    # DATE FORMAT: MONTH_DAY_YEAR - HOUR_MINUTES_SECONDS
    timestamps = datetime.datetime.now().strftime('%m_%d_%y %H_%M_%S')
    timestamp = datetime.datetime.now().strftime('%m_%d_%y')

    # CLICKING AGREEMENTS AND PREFERENCES:
    # CLICK AGE AGREEMENT BUTTON
    click = driver.find_element(By.CSS_SELECTOR, "#ageagree")
    driver.execute_script("arguments[0].click();", click)
    driver.implicitly_wait(10)

    # CLICK UNITED STATES
    us = driver.find_element("id", "ac-United States")
    driver.execute_script("arguments[0].click();", us)
    driver.implicitly_wait(10)

    # CLICK FLORIDA
    fl = driver.find_element("id", "ac-Florida")
    driver.execute_script("arguments[0].click();", fl)
    driver.implicitly_wait(10)

    # CLICK FORT MYERS
    fort_myers = driver.find_element(By.XPATH, '//*[@id="choseCityContainer"]/div[3]/article/div[10]/article/p[3]/a')
    driver.execute_script("arguments[0].click();", fort_myers)
    driver.implicitly_wait(10)

    # CLICK WOMEN SEARCHING MALE
    women_seeking_male = driver.find_element(By.XPATH, '//*[@id="megapCategoriesOrangeButton"]/a')
    driver.execute_script("arguments[0].click();", women_seeking_male)
    driver.implicitly_wait(10)

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
            driver.implicitly_wait(10)

        pageCounter += 1

    link_counter = 0

    for link in links:
        print(f"Processing link {link_counter}: {link}")  # Debugging print statement
        driver.get(link)
        driver.implicitly_wait(10)
        for keyword in selected_keywords:
            description = driver.find_element(By.CSS_SELECTOR, 'body > div > div.post_preview_body > span').text
            driver.implicitly_wait(10)
            if keyword in description.lower():
                page_url = driver.current_url
                driver.implicitly_wait(10)

                title = driver.find_element(By.CLASS_NAME, 'post_preview_title').text
                driver.implicitly_wait(10)

                description = driver.find_element(By.CLASS_NAME, 'postbody').text
                driver.implicitly_wait(10)

                age = driver.find_element(By.CLASS_NAME, 'post_preview_age').text
                driver.implicitly_wait(10)

                phone_number = driver.find_element(By.CSS_SELECTOR,
                                                   'body > div > div.post_preview_body > '
                                                   'div.fromLeft.post_preview_phone'
                                                   '> span > a').get_attribute(
                    "innerHTML")
                driver.implicitly_wait(10)

                # APPEND CONTENTS TO LIST
                LIST.append([link_counter, page_url, title, age, description, phone_number, keyword])

                # SET SCREENSHOT SIZE
                S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
                driver.set_window_size(S('Width'), S('Height'))

                # SCREENSHOT LISTING
                screenshot_name = f"({link_counter})_{timestamps}_megapersonals.png"
                # MAKE DIRECTORY FOR SCREENSHOTS
                screenshot_dir = pathlib.Path.home() / f"Desktop/megapersonals/ft_myers/screenshots/{timestamp}"
                if not os.path.exists(screenshot_dir):
                    os.makedirs(screenshot_dir)
                driver.save_screenshot(screenshot_dir/f"{screenshot_name}")
                break

        link_counter += 1

    # SET UP COLUMNS FOR EXCEL FILE
    columns = ('screenshot number', 'url', 'title', 'age', 'description', 'phone number', 'matching keyword')
    df = pd.DataFrame(LIST, columns=columns)

    # EXPORT TO EXCEL FILE
    excel_dir = pathlib.Path.home() / f"Desktop/megapersonals/ft_myers/excel_files/{timestamp}"
    os.mkdir(excel_dir)
    df.to_excel(excel_dir/f"megapersonals({timestamps}).xlsx", index=False)
    print(f'megapersonals({timestamps}).xlsx exported.')

    # CLOSE WEBDRIVER
    driver.close()
