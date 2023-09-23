# get random image download link from Unsplash based on given string
from pyunsplash import PyUnsplash
import requests
import glob
import os
import pandas as pd
from PIL import Image, ImageFont, ImageDraw
import sys
import openai

search_query = sys.argv[1]
UNSPLASH_ACCESS_KEY = sys.argv[2]
USER_NAME = sys.argv[3]
CUSTOM_MESSAGE = sys.argv[4]
try:
    OPEN_AI_KEY = sys.argv[5]
except:
    OPEN_AI_KEY = ""
project_path = os.path.normpath('')

# get random image download link from Unsplash based on given string
pu = PyUnsplash(api_key=UNSPLASH_ACCESS_KEY)
photos = pu.photos(type_='random', count=1, featured=True,
                   orientation='landscape', query=search_query)
[photo] = photos.entries
print(photo.id, photo.link_download)

# download required image from unsplash
images_path = os.path.join(project_path, 'images')
response = requests.get(photo.link_download, allow_redirects=True)
temp_image = os.path.join(images_path, 'img_temp.png')
open(temp_image, 'wb').write(response.content)

# openai function
def get_completion(prompt):
    openai.api_key = OPEN_AI_KEY
    model="gpt-3.5-turbo"
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message["content"]

# get random birthday message
data_path = os.path.join(project_path, 'data')
if '.csv' in CUSTOM_MESSAGE:
    df = pd.read_csv(os.path.join(data_path, CUSTOM_MESSAGE))
    CUSTOM_MESSAGE = df.loc[df.sample().index, 'message'].to_numpy()[0]
    print(CUSTOM_MESSAGE)
elif 'openai' in CUSTOM_MESSAGE:
    message = CUSTOM_MESSAGE.replace('openai ', '')
    prompt = "generate an " + message + " wish in about 70 characters. make it enthusiastic and formal. do not add any emojis."
    CUSTOM_MESSAGE = get_completion(prompt)
    print(CUSTOM_MESSAGE)

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
font_ttf = os.path.join(data_path, 'Hey August.ttf')
font_size = 75
if len(CUSTOM_MESSAGE) > 70:
    font_size = 55
font_x_pos = 80
font_y_pos = 80
font_color = "white"
font_bgcolor = "black"

final_image = os.path.join(images_path, 'wish.png')
image = Image.open(temp_image)
image.thumbnail((720, 1024), Image.LANCZOS)
w, h = image.size

draw_image = ImageDraw.Draw(image)
image_font = ImageFont.truetype(font_ttf, font_size)
image_bgfont = ImageFont.truetype(font_ttf, font_size)

# thin border
# draw_image.text((font_x_pos-1, font_y_pos), get_wrapped_text(CUSTOM_MESSAGE, image_font, w-100), font=image_font, fill=font_bgcolor)
# draw_image.text((font_x_pos+1, font_y_pos), get_wrapped_text(CUSTOM_MESSAGE, image_font, w-100), font=image_font, fill=font_bgcolor)
# draw_image.text((font_x_pos, font_y_pos-1), get_wrapped_text(CUSTOM_MESSAGE, image_font, w-100), font=image_font, fill=font_bgcolor)
# draw_image.text((font_x_pos, font_y_pos+1), get_wrapped_text(CUSTOM_MESSAGE, image_font, w-100), font=image_font, fill=font_bgcolor)

# thicker border
draw_image.text((font_x_pos-2, font_y_pos-2), get_wrapped_text(CUSTOM_MESSAGE, image_bgfont, w-100), font=image_font, fill=font_bgcolor)
draw_image.text((font_x_pos+2, font_y_pos-2), get_wrapped_text(CUSTOM_MESSAGE, image_bgfont, w-100), font=image_font, fill=font_bgcolor)
draw_image.text((font_x_pos-2, font_y_pos+2), get_wrapped_text(CUSTOM_MESSAGE, image_bgfont, w-100), font=image_font, fill=font_bgcolor)
draw_image.text((font_x_pos+2, font_y_pos+2), get_wrapped_text(CUSTOM_MESSAGE, image_bgfont, w-100), font=image_font, fill=font_bgcolor)

# add text
draw_image.text((font_x_pos, font_y_pos), get_wrapped_text(CUSTOM_MESSAGE, image_font, w-100), font=image_font, fill=font_color)


# add brand
brand = "@testingchief"
brand_font_ttf = os.path.join(data_path, 'Spicy Pizza.ttf')
brand_font = ImageFont.truetype(brand_font_ttf, 15)
brand_font_color = "#9C9C9C"
draw_image.text((w-100, h-20), brand, fill=brand_font_color, font=brand_font)

# save generated image
image.save(final_image)
