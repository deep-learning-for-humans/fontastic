import ast
import traceback
import argparse
import configparser
import os
import sys
from torchvision import transforms
from PIL import Image

from fontastic import LOGGER


def random_crop(image_path, width, height, number_of_random_crops=5):
    '''[summary]
    
    Arguments:
        image {[type]} -- [description]
        width {[type]} -- [description]
        height {[type]} -- [description]
    '''
    try:
        LOGGER.info("Processing font img {} and cropping it into size {}".format(
            image_path, (width, height)))
        pil_image = Image.open(image_path)
        for i in range(number_of_random_crops):
            random_crop = transforms.RandomCrop(size=(width, height))
            random_crop_image = random_crop.__call__(pil_image)
            out_file = pil_image.filename.split(
                '.')[0] + 'random_crop_' + str(i) + '.jpg'
            LOGGER.info("Writing to file {}".format(out_file))
            random_crop_image.save(out_file, quality=95, dpi=(300, 300))
    except Exception as e:
        LOGGER.error(traceback.format_exc())


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Argument for generating random crops')
    arg_parser.add_argument('--config', type=str,
                            help='Path to configuration file')

    if not len(sys.argv) > 1:
        LOGGER.info(
            "Please pass the required command line arguments, use python module -h for help")
        exit()

    arguments = arg_parser.parse_args()
    config_file_path = arguments.config
    LOGGER.info("Configuration path is {}".format(config_file_path, ))

    config = configparser.ConfigParser()
    config.read(config_file_path)

    config_section = config['TRAINING_DATA']
    font_base_dir = config_section['base_dir']
    number_of_random_crops = ast.literal_eval(
        config_section['number_of_random_crops'])
    width = ast.literal_eval(config_section['width'])
    height = ast.literal_eval(config_section['height'])

    for font_dir in os.listdir(font_base_dir):
        LOGGER.info("Processing font directory {}".format(font_dir))
        font_dir = os.path.join(font_base_dir, font_dir)
        if os.path.isdir(font_dir):
            for font_img in os.listdir(font_dir):
                font_img = os.path.join(font_dir, font_img)
                random_crop(font_img, width, height,
                            number_of_random_crops=number_of_random_crops)
