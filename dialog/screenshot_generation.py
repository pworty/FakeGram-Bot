import requests
from string import Template
from bot_data import USER_ID, API_KEY
from dialog.default_images_links import *

with open('dialog.html', 'r') as f:
    html = Template(f.read())

with open('dialog.css', 'r') as f:
    css = f.read()

html = html.substitute(bot_welcome_background_1=bot_welcome_background_1,
                       bot_welcome_bluetooth=bot_welcome_bluetooth,
                       bot_welcome_chevron=bot_welcome_chevron,
                       bot_welcome_rectangle_3=bot_welcome_rectangle_3,
                       contact_search_query_background_1=contact_search_query_background_1,
                       contact_search_query_wifi=contact_search_query_wifi,
                       dialog_avatar=dialog_avatar,
                       dialog_background=dialog_background,
                       dialog_background_image=dialog_background_image,
                       dialog_combined_shape=dialog_combined_shape,
                       dialog_mobile_signal=dialog_mobile_signal,
                       dialog_oval=dialog_oval,
                       dialog_oval_3=dialog_oval_3,
                       dialog_part_1=dialog_part_1,
                       dialog_path_3_1=dialog_path_3_1,
                       dialog_path_3_copy_1=dialog_path_3_copy_1,
                       dialog_path_4=dialog_path_4,
                       dialog_telegram_attachement=dialog_telegram_attachement)

HCTI_API_ENDPOINT = "https://hcti.io/v1/image"
HCTI_API_USER_ID = USER_ID
HCTI_API_KEY = API_KEY
data = {'html': html, 'css': css, 'google_fonts': "Helvetica",
        'viewport_width': 1, 'viewport_height': 1}

image = requests.post(url=HCTI_API_ENDPOINT, data=data, auth=(HCTI_API_USER_ID, HCTI_API_KEY))
print(image.json()['url'])
