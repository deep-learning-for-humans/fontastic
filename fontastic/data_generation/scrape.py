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


def get_specimen_urls(html, font_variant_base_url):
    """Using the font main page, get the hash for every font variant
    Example returns the list of hashes for every variant of Roboto

    Arguments:
        html {string} -- Raw HTML

    Returns:
        list -- list of hash values of font variants
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')

        select = soup.find(id="specimen_select")
        options = select.find_all("option")

        return [font_variant_base_url + opt.get("value") for opt in options]
    except:
        raise


def get_specimen_images(html):
    """Generator which yields the image to be downloaded.
    This function parses the specimen page html, finds all <img>, fetches the image via requests

    Arguments:
        html {string} -- HTML page of fontsquirel specimen page. Example - https://www.fontsquirrel.com/fonts/ajax/specimen_images/3fcbdb4c29e43e3a56918081e68319e1
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        imgs = soup.find_all("img")

        for img in imgs:
            yield requests.get(img.get("src"), stream=True, allow_redirects=True)
    except:
        raise


def fetch_font_variants(url, font_name, output_dir):
    """Fetch the specimen image of the font variant using the url & save it as png

    Arguments:
        url {string} -- url for the font variant image
    """
    res = requests.get(url)

    if res.status_code == 200:
        font_output_dir = os.path.join(output_dir, font_name)
        if not os.path.exists(font_output_dir):
            os.makedirs(font_output_dir)
        for image in get_specimen_images(res.text):
            image_file_name = os.path.join(
                font_output_dir, 'img-{}-{}.png'.format(font_name, dt.now()))
            LOGGER.info("Writing to file {}".format(image_file_name,))
            with open(image_file_name, 'wb') as out_file:
                shutil.copyfileobj(image.raw, out_file)


def load_font_main(font_name, font_main_base_url, font_variant_base_url, output_dir):
    """load the main page for a font on font squirel

    Arguments:
        font_name -- roboto / open-sans etc
    """
    try:
        LOGGER.info("start {}".format(font_name))
        request_url = font_main_base_url + font_name
        LOGGER.info("Fetching data for font {} from url : {}".format(
            font_name, font_main_base_url))
        res = requests.get(request_url)
        if res.status_code == 200:
            # process html
            urls = get_specimen_urls(res.text, font_variant_base_url)
            for url in urls:
                fetch_font_variants(url, font_name, output_dir)
            LOGGER.info("Finished fetching data for font {}".format(font_name))
        else:
            LOGGER.error("Fetching data for font {} failed".format(font_name,))
    except:
        raise


def gather_data(font_list, font_main_base_url, font_variant_base_url, output_dir, pool_size):
    ''' Parallel fetches the images for different fonts provided in the list
    Arguments:
        font_list {list} -- List containing all the font names
        font_main_base_url {str} --  Main base url for fetching the font images
        font_variant_base_url {str} -- Base url for fetching the variants of the fonts
        output_dir {str} --  Path to the directory where the images are stored
        pool_size {int} -- Number of parallel processes 
    '''

    try:
        pool = mp.Pool(processes=pool_size)
        pool_processing = [pool.apply_async(load_font_main, args=(
            font, font_main_base_url, font_variant_base_url, output_dir)) for font in font_list]
        results = [process.get() for process in pool_processing]

    except:
        LOGGER.exception(traceback.format_exc())


if __name__ == '__main__':

    '''
    Setting command lines argument parser for reading path to configuration file
    '''

    arg_parser = argparse.ArgumentParser(
        description='Arguments for the data scraper')
    arg_parser.add_argument('--config',  type=str,
                            help='Path to configuration file')
    arguments = arg_parser.parse_args()
    config_file_path = arguments.config
    LOGGER.info("Configuration path is {}".format(config_file_path, ))

    config = configparser.ConfigParser()
    config.read(config_file_path)

    font_section = config['FONTS']
    required_font_list = ast.literal_eval(font_section.get('required_fonts'))
    font_main_base_url = font_section['font_main_base']
    font_variant_base_url = font_section['font_variant_base']
    LOGGER.debug(" Font list {} is of type {}".format(
        required_font_list, type(required_font_list)))

    config_section = config['CONFIG']
    output_dir = config_section['output_dir']
    pool_size = ast.literal_eval(config_section['multiprocessing_pool_size'])

    LOGGER.debug("Pool size {} is of type {}".format(
        pool_size, type(pool_size)))
    gather_data(font_list=required_font_list, font_main_base_url=font_main_base_url,
                font_variant_base_url=font_variant_base_url, output_dir=output_dir, pool_size=pool_size)
