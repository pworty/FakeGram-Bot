import requests
from string import Template
from random import randrange
from dialog.default_images_links import *
from bot_data import HCTI_API_ENDPOINT, HCTI_API_USER_ID, HCTI_API_KEY


def screenshot_generation(user_data, method_names):
    with open('dialog/dialog.html', 'r') as f:
        html = Template(f.read())

    with open('dialog/dialog.css', 'r') as f:
        css = Template(f.read())

    html = html.substitute(bot_welcome_background_1=bot_welcome_background_1,
                           bot_welcome_bluetooth=bot_welcome_bluetooth,
                           bot_welcome_chevron=bot_welcome_chevron,
                           bot_welcome_rectangle_3=bot_welcome_rectangle_3,
                           contact_search_query_background_1=contact_search_query_background_1,
                           contact_search_query_wifi=contact_search_query_wifi,
                           dialog_combined_shape=dialog_combined_shape,
                           dialog_mobile_signal=dialog_mobile_signal,
                           dialog_oval=dialog_oval,
                           dialog_oval_3=dialog_oval_3,
                           dialog_part_1=dialog_part_1,
                           dialog_path_3_1=dialog_path_3_1,
                           dialog_path_3_copy_1=dialog_path_3_copy_1,
                           dialog_path_4=dialog_path_4,
                           dialog_telegram_attachement=dialog_telegram_attachement,
                           time=user_data[method_names['Time']],
                           battery=user_data[method_names['Battery']],
                           background=user_data[method_names['Background']],
                           name=user_data[method_names['Name']],
                           last_online=user_data[method_names['Last']],
                           avatar=user_data[method_names['Avatar']])

    css = css.substitute()

    viewport = randrange(1, 101)
    # I have absolutely no idea why it has to be done this way,
    # but otherwise image wouldn't generate properly every time,
    # so because it is a gamble, we need random numbers!

    data = {'html': html, 'css': css, 'google_fonts': "Helvetica",
            'viewport_width': viewport, 'viewport_height': viewport}
    image = requests.post(url=HCTI_API_ENDPOINT, data=data, auth=(HCTI_API_USER_ID, HCTI_API_KEY))
    URL = image.json()['url']
    return URL
