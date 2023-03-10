# This version adds a quick parser (link parser) to grab the base url out of a list of urls that
# were received during a Google search and print text to file.

# RUNNING THE CODE: run the code in terminal using the
# following query: python safe_place.py -s site -q query
import argparse
import sys
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
import pandas as pd

# version number
# and functions for dispatch table
VERSION = 3.05

# these globals would become class params once this made into a class
site = ""
query = ""
depth = 0


# current issue (1/3/23):
# 
#
def search_skip_the_games(searchterms):
    """
    searches skipthegames for a keyword
    :param searchterms: The term to search for
    :return: the fully built query string
    """
    searchterms = "+".join(searchterms.split())
    # query: https://skipthegames.com/posts/fort-myers/?keywords=meetup

    url = f'https://skipthegames.com/posts/fort-myers/?keywords={searchterms}'
    # different query for keywords with spaces
    # https://skipthegames.com/posts/fort-myers/?keywords=meet+up

    soup = BeautifulSoup(get_response(url), 'html.parser')
    for link in soup.find_all("p"):
        print(link.text)
        return link.text


# current issue (1/2/23): cannot follow the link, search query is complicated
# invalid URL error code - 'refresh the page'
def search_craigslist(searchterms):
    """
    searches craigslist for a keyword
    :param searchterms: The term to search for
    :return: the fully built query string
    """
    searchterms = "+".join(searchterms.split())
    # query: https://fortmyers.craigslist.org/search/hhh?query=meetup

    url = f'https://fortmyers.craigslist.org/search/hhh?query={searchterms}'
    # different query for keywords with spaces
    # https://fortmyers.craigslist.org/search/hhh?query=meet+up

    soup = BeautifulSoup(get_response(url), 'html.parser')
    for link in soup.find_all("p"):
        print(link.text)
        return link.text


# current issue (1/2/23): search query is returning an invalid URL
def search_megapersonals(searchterms):
    """
    searches craigslist for a keyword
    :param searchterms: The term to search for
    :return: the fully built query string
    """
    searchterms = "+".join(searchterms.split())
    # query: https://megapersonals.eu/public/post_list/234/1/1/meetup

    url = f'https://megapersonals.eu/public/post_list/234/1/1/{searchterms}'

    soup = BeautifulSoup(get_response(url), 'html.parser')
    for link in soup.find_all("p"):
        print(link.text)
        return link.text


# main sites to search with query strings
# will have to make this a full dispatch table to custom functions later
sites = {
    "skipthegames": search_skip_the_games,
    "craigslist": search_craigslist,
    "megapersonals": search_megapersonals
}


def init() -> str:
    sysargs = argparse.ArgumentParser(description="loads passed url to file after initial cleaning (munging).")
    sysargs.add_argument("-v", "--version", action="version", version=f"Current version is {VERSION}")
    sysargs.add_argument("-s", "--site", help="the site to search (google, wikipedia, gutenberg, amazon)")
    sysargs.add_argument("-q", "--query", help="the term(s) to search for.")
    sysargs.add_argument("-d", "--depth", help="follow the nth result, limited to five results.")
    args = sysargs.parse_args()

    # check that all arguments were passed and add site as our global variable
    global site
    global query
    site = str(args.site).lower()

    try:
        if args.query:
            query = args.query
            return sites.get(site)(query)
        else:
            print("must provide both the site (-s,--site) and query string (-q,--q) to use this program.")
            quit(1)
    except (KeyError, TypeError) as ex:
        print("acceptable sites to search for are: google, wikipedia(wiki), amazon, gutenberg(books)")
        quit(1)


headers = {
    'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36 Edg/108.0.1462.54'
}


def get_response(uri):
    # search get and return a response from the url provided

    # Gets website url and provides response
    # If error - exits with exception
    try:
        response = requests.get(uri, headers=headers)
        response.raise_for_status()
    except HTTPError as httperr:
        print(f'HTTP error: {httperr}')
        sys.exit(1)
    except Exception as err:
        print(f"something went wrong: {err}")
        sys.exit(1)

    return response.text


if __name__ == '__main__':
    url = init()
    print(f"data written to, {site}_{query}.txt")
    if get_response(url):
        # writing the results to a file - formatted (site_query.txt)
        with open(f"{site}_{query}.txt", "w", encoding="utf-8") as f:
            f.write(get_response(url))
    else:
        print("first link was un-followable or no links found.")
