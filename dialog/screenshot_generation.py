import requests
from string import Template
from random import randrange
from dialog.default_images_links import *
from bot_data import HCTI_API_ENDPOINT, HCTI_API_USER_ID, HCTI_API_KEY


def screenshot_generation(user_data, method_names):
    with open('dialog/dialog.html', 'r') as f:
        dialog_html = Template(f.read())

    with open('dialog/interlocutor_message.html', 'r') as f:
        interlocutor_message_html = Template(f.read())

    with open('dialog/user_message.html', 'r') as f:
        user_message_html = Template(f.read())

    with open('dialog/dialog.css', 'r') as f:
        dialog_css = Template(f.read())

    with open('dialog/interlocutor_message.css', 'r') as f:
        interlocutor_message_css = Template(f.read())

    with open('dialog/user_message.css', 'r') as f:
        user_message_css = Template(f.read())

    total_lines = 0
    interlocutor_messages_html = []
    user_messages_html = []
    interlocutor_messages_css = []
    user_messages_css = []
    for i in range(1, user_data['message_count'] + 1):
        total_lines += user_data[f'message_{i}_lines']
        if user_data[f'message_{i}_sender'] == 'Interlocutor':
            interlocutor_message_html_string = interlocutor_message_html.substitute(
                i=i, message=user_data[f'message_{i}_text'], time=user_data[f'message_{i}_time'])
            interlocutor_message_css_string = interlocutor_message_css.substitute(
                i=i, total_lines=total_lines, lines=user_data[f'message_{i}_lines'])
            interlocutor_messages_html.append(interlocutor_message_html_string)
            interlocutor_messages_css.append(interlocutor_message_css_string)
        else:
            user_message_html_string = user_message_html.substitute(
                i=i, message=user_data[f'message_{i}_text'], time=user_data[f'message_{i}_time'])
            user_message_css_string = user_message_css.substitute(
                i=i, total_lines=total_lines, lines=user_data[f'message_{i}_lines'])
            user_messages_html.append(user_message_html_string)
            user_messages_css.append(user_message_css_string)

    interlocutor_messages_html_string = '\n'.join(interlocutor_messages_html)
    user_messages_html_string = '\n'.join(user_messages_html)
    interlocutor_messages_css_string = '\n'.join(interlocutor_messages_css)
    user_messages_css_string = '\n'.join(user_messages_css)

    dialog_html = dialog_html.substitute(interlocutor_messages=interlocutor_messages_html_string,
                                         user_messages=user_messages_html_string,
                                         time=user_data[method_names['Time']],
                                         battery=user_data[method_names['Battery']],
                                         background=user_data[method_names['Background']],
                                         name=user_data[method_names['Name']],
                                         last_online=user_data[method_names['Last']],
                                         avatar=user_data[method_names['Avatar']])

    dialog_css = dialog_css.substitute(interlocutor_messages=interlocutor_messages_css_string,
                                       user_messages=user_messages_css_string)

    # Log final code
    with open('dialog/dialog_final.html', 'w') as f:
        f.write(dialog_html)

    with open('dialog/dialog_final.css', 'w') as f:
        f.write(dialog_css)

    viewport = randrange(1, 101)  # has to be less than background image size
    # I have absolutely no idea why it has to be done this way,
    # but otherwise image wouldn't generate properly every time,
    # so because it's a gamble, we need random numbers!

    data = {'html': dialog_html, 'css': dialog_css, 'google_fonts': "Helvetica",
            'viewport_width': viewport, 'viewport_height': viewport}
    image = requests.post(url=HCTI_API_ENDPOINT, data=data, auth=(HCTI_API_USER_ID, HCTI_API_KEY))
    URL = image.json()['url']
    return URL
