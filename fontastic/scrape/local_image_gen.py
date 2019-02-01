from PIL import Image, ImageDraw, ImageFont
# import ttfquery.findsystem 
import string
import ntpath
import numpy as np
import os
import glob

fontSize = 40
imgSize = (1200,50)
position = (0,0)

#All images will be stored in 'Synthetic_dataset' directory under current directory
dataset_path = os.path.join (os.getcwd(), 'synthetic_dataset')
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

lower_case_list = list(string.ascii_lowercase)
upper_case_list = list(string.ascii_uppercase)
digits = range(0,10)

digits_list=[]
for d in digits:
    digits_list.append(str(d))

all_char_list = lower_case_list + upper_case_list + digits_list

fonts_list = ['Roboto']
# for line in fhandle:
#    fonts_list.append(line.rstrip('\n'))

total_fonts = len(fonts_list)
#paths = ttfquery.findsystem.findFonts()
all_fonts = glob.glob(os.path.join (os.getcwd(), 'data', 'fonts', 'roboto', '*.ttf'))
# all_fonts = glob.glob("C:\\Windows\\Fonts\\*.ttf")
f_flag = np.zeros(total_fonts)

print(all_fonts) 

for sys_font in all_fonts:
    #print "Checking "+p
   font_file = ntpath.basename(sys_font)
   font_file = font_file.rsplit('.')
   font_file = font_file[0]
   f_idx = 0
   for font in fonts_list:
    #   f_lower = font.lower()
      s_lower = sys_font.lower()
      #Check desired font
    #   if f_lower in s_lower:
      path = sys_font
      font_ttf = ImageFont.truetype(path, fontSize)
      f_flag[f_idx] = 1

      text_types = ["""the quick brown fox jumped the lazy dog""",
              """a b c d e f g h i j k l m n o p q r s t u v w x y z""",
              """1 2 3 4 5 6 7 8 9 0"""
              ]

      for idx, ch in enumerate(text_types):
          image = Image.new("RGB", imgSize, (255,255,255))
          draw = ImageDraw.Draw(image)
          pos_x = 0
          pos_y = 0
          pos_idx=0
        #   for y in [pos_y-1, pos_y, pos_y+1]:
        #       for x in [pos_x-1, pos_x, pos_x+1]:
          position = (pos_x, pos_y)
          print(font)
          print(font_ttf)
          draw.text(position, ch, (0,0,0), font=font_ttf)

          file_name = font_file + '_' + str(idx) + '_' + '.jpg'
          file_name = os.path.join(dataset_path,file_name)
          image.save(file_name, quality=95, dpi=(600,600))
          pos_idx = pos_idx + 1
      f_idx = f_idx + 1
