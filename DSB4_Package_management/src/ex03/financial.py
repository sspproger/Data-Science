#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import sys
import time
import re

def parse_html(response, field):
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.find_all('div', {'class': re.compile('row lv-0')})
    if not rows:
        raise Exception('Financial data table not found for the given ticker')

    for row in rows:
        financial_field = row.find('div', {'class': re.compile('rowTitle')})
        if financial_field and financial_field.text.strip() == field:
                values = row.find_all('div', {'class': re.compile('column yf-')})
                txt = [value.text.strip() for value in values]
                return (txt)

    raise Exception(f'Financial field "{field}" not found in the statement') 

def main():
    try:
        ticker = sys.argv[1]
        field = sys.argv[2]
        url = f'https://finance.yahoo.com/quote/{ticker}/financials'
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 YaBrowser/25.12.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f'Failed to fetch data (HTTP status code: {response.status_code})')
        values = parse_html(response, field)
        time.sleep(5)
        print((field, *values))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()