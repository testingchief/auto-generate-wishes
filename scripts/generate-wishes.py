### get random image download link from Unsplash based on given string
from pyunsplash import PyUnsplash
import requests
import glob
import os
import pandas as pd
from PIL import Image, ImageFont, ImageDraw
import sys

search_query = sys.argv[1]
UNSPLASH_ACCESS_KEY = sys.argv[2]
USER_NAME = sys.argv[3]
project_path = os.path.normpath('')

# get random image download link from Unsplash based on given string
pu = PyUnsplash(api_key=UNSPLASH_ACCESS_KEY)
photos = pu.photos(type_='random', count=1, featured=True, orientation='landscape', query=search_query)
[photo] = photos.entries
print(photo.id, photo.link_download)

# download required image from unsplash
images_path = os.path.join(project_path, 'images')
response = requests.get(photo.link_download, allow_redirects=True)
temp_image = os.path.join(images_path, 'img_temp.png')
open(temp_image, 'wb').write(response.content)

# get random birthday message
data_path = os.path.join(project_path, 'data')
df = pd.read_csv(os.path.join(data_path, 'birthday_msg.csv'))
text_to_write = df.loc[df.sample().index, 'birthday_msg'].to_numpy()[0]
print(text_to_write)

# reusable method to get wrapped text
def get_wrapped_text(text: str, font: ImageFont.ImageFont,
                     line_length: int):
        lines = ['']
        for word in text.split():
            line = f'{lines[-1]} {word}'.strip()
            if font.getlength(line) <= line_length:
                lines[-1] = line
            else:
                lines.append(word)
        lines.append(" - " + USER_NAME)
        return '\n'.join(lines)

# write text to downloaded image
font_ttf = os.path.join(data_path, 'The California.ttf')
font_size = 100
if len(text_to_write)>70:
     font_size = 90
font_x_pos = 60
font_y_pos = 50
font_bg_x_pos = 59
font_bg_y_pos = 49

font_color = "#000000" #black
# font_bgcolor = "#9133FF" #purple
font_bgcolor = "#FFFF33" #yellow

# font_color = "#ffffff" #white
# font_bgcolor = "#333BFF" #black

final_image = os.path.join(images_path, 'wish.png')
image = Image.open(temp_image)
image.thumbnail((1024,1024), Image.LANCZOS)
draw_image = ImageDraw.Draw(image)
image_font = ImageFont.truetype(font_ttf,font_size)

draw_image.text((font_bg_x_pos,font_bg_y_pos), get_wrapped_text(text_to_write, image_font, 500), fill=font_bgcolor, font=image_font)
draw_image.text((font_x_pos,font_y_pos), get_wrapped_text(text_to_write, image_font, 500), fill=font_color, font=image_font)

image.save(final_image)
