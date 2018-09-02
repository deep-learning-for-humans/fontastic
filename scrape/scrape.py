import shutil
from datetime import datetime as dt
import requests
from bs4 import BeautifulSoup

font_main_base = "https://www.fontsquirrel.com/fonts/"
font_variant_base = "https://www.fontsquirrel.com/fonts/ajax/specimen_images/"


def get_specimen_urls(html):
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

        return [font_variant_base + opt.get("value") for opt in options]
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


def fetch_font_variants(url, font_name):
    """Fetch the specimen image of the font variant using the url & save it as png

    Arguments:
        url {string} -- url for the font variant image
    """
    res = requests.get(url)

    if res.status_code == 200:
         for image in get_specimen_images(res.text):
             print(image)
             with open('img-{}-{}.png'.format(font_name, dt.now()), 'wb') as out_file:
                shutil.copyfileobj(image.raw, out_file)


def load_font_main(font_name):
    """load the main page for a font on font squirel
    
    Arguments:
        font_name -- roboto / open-sans etc
    """
    try:
        print("start {}".format(font_name))
        res = requests.get(font_main_base + font_name)
        if res.status_code == 200:
            # process html
            urls = get_specimen_urls(res.text)

            for url in urls:
                fetch_font_variants(url, font_name)
        print("done {}".format(font_name))
    except:
        raise


if __name__ == '__main__':
    load_font_main('roboto')
    load_font_main('open-sans')
    load_font_main('lato')
    load_font_main('montserrat')
    load_font_main('oswald')
    load_font_main('raleway')
    load_font_main('slabo')
    load_font_main('merriweather')
