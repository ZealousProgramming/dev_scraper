#!/usr/bin/env python3

import re

import requests
from bs4 import BeautifulSoup

# Keywords to search for
LISTING_KEYWORDS = ['Developer', 'Programmers']

# Company names
BSI_NAME = 'Berkeley Springs Instruments(BSI)'
EL_NAME = 'Exclamation Labs'
WT_NAME = 'Willets Tech'

# URL to scrape
BSI_URL = 'http://www.bsisentry.com/career'
EL_URL = 'https://exclamationlabs.recruitee.com/'
WT_URL = 'https://www.willettstech.com/jobs/'


def scrap_url(url: str, keywords: list = None) -> list:
    """ Attempts to retrieve the HTML from the requested url and returns a list
    if any results are found for the passed keywords. The returned list will be
    empty if none of the keywords are found.
    """

    if keywords is None:
        keywords = LISTING_KEYWORDS

    result = requests.get(url)
    doc = BeautifulSoup(result.text, 'html.parser')

    results: list = []

    for keyword in keywords:
        result = doc.find_all(text=re.compile(keyword))

        if len(result) != 0:
            results.extend(
                [string.strip() for string in result if string not in results]
            )

    return results


class Company:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.listings = []

    def set_listings(self, new_value=None):
        self.listings = new_value

    def print_listings(self):
        print(f'Job listings for {self.name}: \n')

        if len(self.listings) == 0:
            print('\tNo job listings for Software Developers was found..')
            return

        for listing in self.listings:
            print(f'\t{listing}')

        print('\n\tListing(s) can be found at:', self.url, '\n')


def main():
    bsi: Company = Company(BSI_NAME, BSI_URL)
    el: Company = Company(EL_NAME, EL_URL)
    wt: Company = Company(WT_NAME, WT_URL)

    bsi.set_listings(scrap_url(BSI_URL))
    el.set_listings(scrap_url(EL_URL))
    wt.set_listings(scrap_url(WT_URL))

    bsi.print_listings()
    el.print_listings()
    wt.print_listings()


if __name__ == '__main__':
    main()
