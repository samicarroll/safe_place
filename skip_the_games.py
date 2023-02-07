import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

timestamps = datetime.datetime.now().strftime('%m_%d_%y %H%M%S')
url = 'https://skipthegames.com/'
driver = webdriver.Chrome()
driver.get(url)
LIST = []

# WAIT FOR ELEMENTS TO BE CLICKABLE
wait = WebDriverWait(driver, 10)

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

# ENTERING FORT MYERS IN CITY
location = driver.find_element(By.NAME, 'input_search_location')
location.send_keys('fort myers')
driver.implicitly_wait(10)

# TODO: KEYWORDS CANNOT BE ENTERED BECAUSE
#  PAGE REFRESHES AND REMOVES LOCATION

# ENTER KEYWORDS
# keywords = driver.find_element(By.NAME, 'input_search_optional_keywords')
# keywords.send_keys('blonde')

# SEARCH LOCATION AND KEYWORDS
location.send_keys(Keys.ENTER)  # search location

# wait.until(EC.element_to_be_clickable((By.ID, 'search_button'))).click()

gallery = driver.find_elements(By.CLASS_NAME, 'clsfds-display-mode gallery')
for ads in gallery:
    posts = driver.find_elements(By.CLASS_NAME, 'day-gallery')
    for post in posts:
        date = driver.find_element(By.CLASS_NAME, 'post-timestamp m10')
        print(date)

        title = driver.find_element(By.CLASS_NAME, 'post-title').text
        print(title)

        description = driver.find_element(By.ID, 'post-body').text
        print(description)

        age = driver.find_element(By.CLASS_NAME, 'tiny secondary radius label ad_display_h3_age')
        print(age)

        driver.get_screenshot_as_file(f"skipthegames({timestamps}).png")

        # APPEND CONTENTS TO LIST
        LIST.append([date, title, description, age])
        time.sleep(1)

# EXPORT TO EXCEL
columns = ('date', 'title', 'description', 'age')
df = pd.DataFrame(LIST, columns=columns)

df.to_excel(f'skipthegames({timestamps}).xlsx', index=False)
print(f'skipthegames({timestamps}).xlsx exported.')
# CLOSE WEBDRIVER
driver.close()
