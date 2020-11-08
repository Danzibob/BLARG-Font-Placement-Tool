import logging
import requests
import jmespath
import shutil
import os
import sqlite3
import hashlib

# bachmanetti spreadsheet (Screaped Responses)
SPREADSHEET_SCRAPED_URL = 'https://spreadsheets.google.com/feeds/cells/1oyesB6iW5zYveN5C-qvwvxpMUCpwMOP7h6psa39mlsM/2/public/full?alt=json'
# SCRAPED_JQ_FILTER = '.feed.entry[] | select(."gs$cell".col == "4" and ."gs$cell".row > "2") | .content."$t"'
SCRAPED_JMES_FILTER = 'feed.entry[?"gs$cell".col==`"4"` && "gs$cell".row>`"2"`].content."$t"'

SPREADSHEET_SRC_URL = 'https://spreadsheets.google.com/feeds/cells/1oyesB6iW5zYveN5C-qvwvxpMUCpwMOP7h6psa39mlsM/2/public/full?alt=json'
# SRC_JQ_FILTER = '.feed.entry[] | select(."gs$cell".col == "5" and ."gs$cell".row > "1") | .content."$t"'
SRC_JMES_FILTER = 'feed.entry[?"gs$cell".col==`"4"` && "gs$cell".row>`"1"`].content."$t"'
EARLY_ACCESS_DENIED_MD5 = 'e1d4105c8bcd488c5f452ec5fb5e8739'

logger = logging.getLogger(__name__)


def find_next_filename(filename):
    counter = 1
    path, name = os.path.split(filename)
    new_name = os.path.join(path, '%s-%s' % (counter, name))
    while os.path.exists(new_name):
        counter += 1
        new_name = os.path.join(path, '%s-%s' % (counter, name))
    return new_name


def download_file(url):
    logger.info('Fetching %s', url)
    local_filename = os.path.join('imgs', url.split('/')[-1])
    if not os.path.exists(local_filename):
        try:
            with requests.get(url) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    f.write(r.content)
        except requests.exceptions.HTTPError as e:
            logger.error('%s', e)
        except:
            return


def main():
    os.makedirs('imgs', exist_ok=True)
    sheet_json = requests.get(SPREADSHEET_SRC_URL).json()
    # print(sheet_json)
    image_urls = jmespath.search(SRC_JMES_FILTER, sheet_json)
    for url in image_urls:
        download_file(url)


if __name__ == "__main__":
    main()