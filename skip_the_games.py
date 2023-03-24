import datetime
import time
import pandas as pd
import undetected_chromedriver
import ssl
import openpyxl
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

def run(keywords):
    ssl._create_default_https_context = ssl._create_unverified_context
    timestamps = datetime.datetime.now().strftime('%m_%d_%y %H%M%S')
    LIST = []
    url = 'https://skipthegames.com/posts/fort-myers'
    visited_urls = []

    headers = {
        'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/107.0.0.0 Safari/537.36',
        'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
        'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/108.0.0.0 Mobile Safari/537.36 Edg/108.0.1462.54'
    }

    driver = undetected_chromedriver.Chrome()
    driver.get(url)
    time.sleep(5)

    wait = WebDriverWait(driver, 10)

    file = open('static/keywords.txt', 'r')
    lines = file.read()
    keywords = lines.split('\n')
    driver.refresh()

    identification = Select(driver.find_element(By.NAME, 'input_search_client'))
    identification.select_by_value('men')
    driver.implicitly_wait(10)

    category = Select(driver.find_element(By.NAME, 'input_search_category'))
    category.select_by_value('female-escorts')
    driver.implicitly_wait(10)
    driver.refresh()

    posts = driver.find_elements(By.CSS_SELECTOR, 'html.no-js body div table.two-col-wrap tbody tr '
                                     'td#gallery_view.listings-with-sidebar.list-search-results.gallery div.full-width '
                                     'div.small-16.columns div.clsfds-display-mode.gallery div.day-gallery [href]')
    dupLinks = [post.get_attribute('href') for post in posts]
    links = [*set(dupLinks)]
    print(links)
    counter = 0
    for urls in links:
        links[:] = (urls for urls in links if not urls.startswith('https://skipthegames.com/reply/meetup/'))
        driver.get(links[counter])

        time.sleep(5)
        description = driver.find_element(By.CSS_SELECTOR, '#post-body > div').text
        for keyword in keywords:
            if keyword in description:
                ad_url = driver.current_url
                print(ad_url)

                title = driver.find_element(By.CLASS_NAME, 'post-title').text
                print(title)

                LIST.append([ad_url, title])

                screenshot_name = f"skipthegames{counter}_keyword_{keyword.replace(' ', '_')}.png"
                driver.save_screenshot(screenshot_name)
                break

        counter += 1

    columns = ('URL', 'Title')
    df = pd.DataFrame(LIST, columns=columns)

    df.to_excel(f'skipthegames({timestamps}).xlsx', index=False)
    print(f'skipthegames({timestamps}).xlsx exported.')

    driver.close()