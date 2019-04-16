import ast
import time
import traceback
import argparse
import configparser
import os
import sys
from torchvision.transforms import Compose, RandomResizedCrop
from sklearn.externals.joblib import Parallel, delayed
from PIL import Image

from fontastic import LOGGER


def random_crop(image_path, font_name, dst_path, width=256, height=256, number_of_random_crops=5):
    '''[summary]
    
    Arguments:
        image {[type]} -- [description]
        width {[type]} -- [description]
        height {[type]} -- [description]
    '''
    try:
        LOGGER.info("Processing font img {} and cropping it into size {}".format(
            image_path, (width, height)))

        # change scale based on the font size
        # pick smaller scale for smaller font size
        # pick large scale for bigger font size
        if image_path.find('_50') > 0 or image_path.find('_80') > 0:
            #TODO move to config
            scale = (0.01, 0.1)
        else:
            scale = (0.1, 0.4)

        tfm = Compose([RandomResizedCrop(size=256, scale=scale)])
        for i in range(number_of_random_crops):
            im = Image.open(image_path)
            random_crop_image = tfm(im)

            #TODO fix & simplify paths & configs
            src_file = image_path.split("/")[-1]
            filename = src_file.split(".")[0]
            out_file = f'{filename}_rand_crop_{i}.jpg'
            out_file = os.path.join(dst_path, out_file)

            LOGGER.info(f'saving file {out_file}')
            random_crop_image.save(out_file, quality=95, dpi=(300, 300))

            # sleep for more diverse random crops
            # TODO really this works??
            time.sleep(0.2)
    except Exception as e:
        raise


def process_font_images(font_dir, img_dst, number_of_random_crops):
    try:
        if os.path.isdir(font_dir):
            for font_img in os.listdir(font_dir):
                font_img = os.path.join(font_dir, font_img)

                # check if dst folder exists
                font_name = font_dir.split("/")[-1]
                dst_font_folder = os.path.join(img_dst, font_name)
                if not os.path.exists(dst_font_folder):
                    LOGGER.info('Destination folder for font missing, will create it, dont worry')
                    os.makedirs(dst_font_folder)
                # LOGGER.info(font_img)
                random_crop(font_img, font_name, dst_font_folder, width, height,
                            number_of_random_crops=number_of_random_crops)

    except Exception as e:
        raise


def process_font(font_dir):
    LOGGER.info("Processing font directory {}".format(font_dir))
    font_dir = os.path.join(font_base_dir, font_dir)
    LOGGER.info(font_dir)
    process_font_images(font_dir, img_dst, number_of_random_crops)


if __name__ == '__main__':
    try:
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
        img_dst = config_section['training_destination']
        
        # parallelize image generation for every font
        Parallel(n_jobs=-2)(delayed(process_font)(fontdir) for fontdir in os.listdir(font_base_dir))

    except Exception as e:
        LOGGER.error(traceback.format_exc())
