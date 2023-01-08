import time
import datetime  # pip install datetime
import requests  # pip install requests
from bs4 import BeautifulSoup  # pip install beautifulsoup4
import pandas as pd  # pip install pandas
import openpyxl  # pip install openpyxl - writes to excel

# scrapes ads from craigslist fort myers - currently searches
# home/rooming section of craigslist


def main(query_url):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        base_url = query_url

        response = requests.get(base_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        total_results = int(soup.find('span', 'totalcount').text)  # find total num. of ads
        total_pages = (total_results // 120) + 1  # find total pages by dividing by total num. of ads per page

        search_results = []

        # for loop to scrape each page
        for i in range(0, total_pages):
            params = {
                's': i * 120  # s used in website search query
            }
            if total_pages == 0:
                print("no results. try another keyword")
            else:
                print('Processing Page {0}'.format(i + 1))
            response = requests.get(base_url, headers=headers, params=params)
            soup = BeautifulSoup(response.content, 'html.parser')

            results = soup.find('ul', {'id': 'search-results'})  # craigslist page results
            result_rows = results.find_all('li', 'result-row')  # result rows

            for result_row in result_rows:
                post_datetime = result_row.time['datetime']  # post date/time
                post_id = result_row.h3.a['data-id']  # id of post
                post_url = result_row.h3.a['href']  # post url
                price = result_row.find('span', 'result-price').text if result_row.find('span', 'result-price') else ''  # ad price
                location = result_row.find('span', 'result-hood').text if result_row.find('span', 'result-hood') else ''  # post location
                post_title = result_row.h3.a.text # post title

                # search result list that will be exported
                search_results.append([
                    post_title, post_datetime, post_id, post_url, price, location
                ])
            time.sleep(1)

        columns = ('title', 'post date', 'post id', 'post url', 'price', 'location')
        df = pd.DataFrame(search_results, columns=columns)

        timestamp = datetime.datetime.now().strftime('%m_%d_%y %H%M%S')
        df.to_excel(f'craigslist_search({timestamp}).xlsx', index=False)
        print('file exported to excel')
    except Exception as e:
        print(e)


keyword = input("enter desired keyword: ")
main(f'https://fortmyers.craigslist.org/search/hsw?query={keyword}&availabilityMode=0')
