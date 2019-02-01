import shutil
from datetime import datetime as dt
import requests
from bs4 import BeautifulSoup
from fontastic import LOGGER
import configparser
import ast
import argparse
import multiprocessing as mp
import traceback
import os
import re

URL_BASE = 'https://www.dafont.com/'

def load_search_page():
    url = f"{URL_BASE}mtheme.php?id=5&fpp=50"
    # fake user agent to mock browser request
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    LOGGER.info("loading search page")
    request_url = url
    res = requests.get(request_url, headers=headers)
    if res.status_code == 200:
        # process html
        print(res.text)
        soup = BeautifulSoup(res.text, 'html.parser')
        font_preview = soup.findAll("div", attrs={"class":"preview"})
        LOGGER.info(font_preview)
        print(font_preview[0].findAll("a")[0].attrs["href"])
        anchors = [div.findAll("a")[0].attrs["href"] for div in font_preview]

        LOGGER.info("{} fonts found from search".format(len(anchors)))

        return anchors

def load_font_page(font):
    url = f"{URL_BASE}{font}&text=the+quick+brown+fox+jumped+the+lazy+dog"

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    LOGGER.info("loading search page")
    request_url = url
    res = requests.get(request_url, headers=headers)
    if res.status_code == 200:
        # process html
        soup = BeautifulSoup(res.text, 'html.parser')
        font_preview = soup.findAll("div", attrs={"class":"preview"})
        bg_img_links = [div.attrs["style"] for div in font_preview]

        LOGGER.info("{} font images found".format(len(bg_img_links)))

        regex = r"\(\/\/(.*)\)"

        image_links = []
        for link in bg_img_links:
            matches = re.finditer(regex, link, re.MULTILINE)
            # LOGGER.debug(f"found {len(matches)} in the url")
            for matchNum, match in enumerate(matches, start=1):
        
                for groupNum in range(0, len(match.groups())):
                    groupNum = groupNum + 1
                    
                    # print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
                    group = match.group(groupNum)
                    image_links.append(group)

    return image_links

# def download_font_images(font, font_urls)

if __name__ == '__main__':

    '''
    Setting command lines argument parser for reading path to configuration file
    '''

    fonts = load_search_page()
    font_url_map = {}
    for font in fonts:
        LOGGER.info(f"start scraping {font}")
        font_image_urls = load_font_page(font)
        LOGGER.info(f"found {len(font_image_urls)} for {font}")

        font_url_map[font] = font_image_urls

    for font in font_url_map.keys():
        print(font)
        print(len(font_url_map[font]))
