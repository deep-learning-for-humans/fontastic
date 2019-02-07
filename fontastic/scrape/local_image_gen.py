from PIL import Image, ImageDraw, ImageFont
# import ttfquery.findsystem 
import string
import ntpath
import numpy as np
import os
import glob

from fontastic.utils.rand_text import RAND_TEXTS

fontSize = 68
imgSize = (3840, 2160)
position = (0,0)

def generate_font_images(font, ttf_path):
    print(os.path.join (ttf_path, '*.ttf'))
    font_files = glob.glob(os.path.join (ttf_path, font, '*.ttf'))
    print(font_files)
    print(f'found {len(font_files)} font file for {font}')

    dst_img_path = os.path.join(dataset_path, font)
    if not os.path.exists(dst_img_path):
        os.makedirs(dst_img_path)
        print(f'creating destination folder for image {font}')

    for font_var in font_files:
        #print "Checking "+p
        font_file = ntpath.basename(font_var)
        font_file = font_file.rsplit('.')
        font_file = font_file[0]

        # font_var = font_var.lower()
        #Check desired font
        #   if f_lower in s_lower:

        text_types = ["""the quick brown fox jumped the lazy dog""",
                """a b c d e f g h i j k l m n o p q r s t u v w x y z""",
                """1 2 3 4 5 6 7 8 9 0"""
                ]

        font_size = {
            0: 300,
            1: 150,
            2: 80,
            3: 50
        }

        # text_types = [RAND_TEXT]

        for idx, ch in enumerate(RAND_TEXTS):
            font_ttf = ImageFont.truetype(font_var, font_size[idx])
            image = Image.new("RGB", imgSize, (255,255,255))
            draw = ImageDraw.Draw(image)
            pos_x = 0
            pos_y = 0

            position = (pos_x, pos_y)
            print(font)
            print(font_ttf)
            print(font_var)
            draw.text(position, ch, (0,0,0), font=font_ttf)

            file_name = font_file + '_' + str(idx) + '_' + '.jpg'
            file_name = os.path.join(dataset_path, font, file_name)
            image.save(file_name, quality=95, dpi=(600,600))

if __name__ == '__main__':
    
    # TODO better logging
    # bootstrapping stuff
    # TODO cleanup later!
    ttf_path = os.path.join (os.getcwd(), 'data', 'src', 'fonts')
    print(ttf_path)
    dataset_path = os.path.join (os.getcwd(), 'data', 'dst')
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    if not os.path.exists(ttf_path):
        print('No fonts files found!')
        exit(-1)

    fonts_list = os.listdir(ttf_path)

    total_fonts = len(fonts_list)
    all_fonts = os.listdir(os.path.join (os.getcwd(), 'data', 'src', 'fonts'))
    all_fonts = [font for font in all_fonts if font != '.DS_Store']
    print(all_fonts) 

    # TODO more clean here with params
    for font in all_fonts:
        # generate_font_images('roboto', ttf_path)
        print(f'generate font image for {font}')
        generate_font_images(font, ttf_path)
