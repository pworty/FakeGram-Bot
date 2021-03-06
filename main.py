import logging

from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import ConversationHandler, CommandHandler

from bot_data import TOKEN, PROXY
from keyboards import *
from dialog.screenshot_generation import screenshot_generation

# from dialog.screenshot_generation import data

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHANGE_PARAM, TIME, BATTERY, BACKGROUND, NAME, \
LAST_ONLINE, LAST_ONLINE_MINUTES, LAST_ONLINE_HOURS, LAST_ONLINE_YESTERDAY, LAST_ONLINE_DATE, \
AVATAR, \
ADD_MESSAGE, ADD_MESSAGE_LINES, ADD_MESSAGE_TIME, ADD_MESSAGE_SENDER, EDIT_MESSAGE, REMOVE_MESSAGE, \
GENERATE = range(18)

method_names = {'Time': TIME, 'Battery': BATTERY, 'Background': BACKGROUND, 'Name': NAME,
                'Last': LAST_ONLINE, 'Avatar': AVATAR, 'Add': ADD_MESSAGE, 'Edit': EDIT_MESSAGE,
                'Remove': REMOVE_MESSAGE, 'Generate': GENERATE}


def start(update, context):
    """update.message.reply_text("Hello! I am FakeGram Bot. I can create fake chats screenshots "
                              "with customization of multiple variables on your screen.\n\n"
                              "What I can do:\n"
                              "/createchat - access screenshot creation menu\n"
                              "(Right now it resets your settings!)\n"
                              "/presets - use one of the presets to creat a fake chat\n"
                              "/settings - configure default time/background/battery and more\n\n"
                              "If you see something like \'Not implemented yet\' or \'Unstable\' "
                              "next to one of Bot's features and you really miss it, feel free to "
                              "contact me by email for sooner release: wortexid@gmail.com",
                              reply_markup=menu_markup)"""

    update.message.reply_text("Hello! I am FakeGram Bot. I can create fake chats screenshots "
                              "with customization of multiple variables on your screen.\n\n"
                              "/createchat - access screenshot creation menu\n"
                              "(Right now it resets your settings!)\n",
                              reply_markup=menu_markup)


def createchat(update, context):
    update.message.reply_text('Alright, now configure settings and press \'Generate\' to get the '
                              'screenshot\n\n'
                              '/cancel to stop screenshot creation. Changes will not be saved!',
                              reply_markup=createchat_markup)
    context.user_data[TIME] = '09:41'
    context.user_data[BATTERY] = '100%'
    context.user_data[
        BACKGROUND] = \
        'https://drive.google.com/uc?id=1ecRZSo2oORvNpnW-1LzrVBf-0L_9NKCa&export=download'
    context.user_data[NAME] = 'Stefan'
    message_sender_keyboard[0][0] = context.user_data[NAME]
    context.user_data[LAST_ONLINE] = 'last seen 5 minutes ago'
    context.user_data[
        AVATAR] = \
        'https://drive.google.com/uc?id=1jE11-wJE2sACh8NvRsQWMVNyR2zTBgnq&export=download'
    context.user_data['message_count'] = 0  # limit is 14 (no overflowing yet)
    return CHANGE_PARAM


def change_param(update, context):
    logger.info(f'context.user_data={context.user_data}')
    message = update.message.text.split()[0]
    if message == 'Time':
        update.message.reply_text('Enter time in "hh:mm" format')
    if message == 'Battery':
        update.message.reply_text('Enter battery percentage from 1 to 100 (no % sign)')
    if message == 'Background':
        update.message.reply_text('Send background image URL (make sure link is public)')
    if message == 'Name':
        update.message.reply_text('Enter the user\'s name')
    if message == 'Last':
        update.message.reply_text('Choose one type from options (Scroll down for more)',
                                  reply_markup=last_seen_markup)
    if message == 'Avatar':
        update.message.reply_text('Send a profile avatar image URL (make sure link is public)\n\n'
                                  'Also make sure avatar is already a circle, '
                                  'otherwise it will be a square (not the best looking)')
    if message == 'Add':
        update.message.reply_text('Enter the message')
    if message == 'Edit':
        update.message.reply_text('Coming soon')
    if message == 'Remove':
        update.message.reply_text('Coming soon')
    if message == 'Generate':
        update.message.reply_text('Choose image format (If one doesn\'t work, try another format)',
                                  reply_markup=image_format_markup)
    if message == '/cancel':
        update.message.reply_text('Stopping screenshot creation', reply_markup=menu_markup)
    return method_names.get(message, message)


def method_value_update(update, context, new, method_name, index):
    old = context.user_data.get(method_name, 'None')
    if method_name != 'Background' and method_name != 'Avatar':
        createchat_keyboard[index[0]][index[1]] = f'{method_name} - {new}'
    else:
        createchat_keyboard[index[0]][index[1]] = f'{method_name} - Custom'
    update.message.reply_text(f'{method_name} updated! ({old} -> {new})',
                              reply_markup=createchat_markup)
    context.user_data[method_names[method_name]] = new


def time(update, context):
    method_name = 'Time'
    index = (0, 0)
    message = update.message.text
    try:
        if ':' in message:
            hh, mm = message.split(':')
        else:
            raise ValueError('":" missing')
        if not (hh.isdigit() and mm.isdigit()):
            raise ValueError('Time is not digits')
        if 1 <= len(hh) <= 2 and 0 <= int(hh) < 24 and len(mm) == 2 and 0 <= int(mm) < 60:
            if len(hh) == 1:
                hh = '0' + hh
            method_value_update(update, context, f'{hh}:{mm}', method_name, index)
            return CHANGE_PARAM
        else:
            raise ValueError('There are only 24 hours in the day, try again')
    except ValueError as e:
        update.message.reply_text(f'Wrong format! {e}')
        logger.warning(f'Value error: {e}: {message}')
        return TIME


def battery(update, context):
    method_name = 'Battery'
    index = (0, 1)
    message = update.message.text
    try:
        if not message.isdigit():
            raise ValueError('Battery % is not digits')
        if 0 < int(message) <= 100:
            method_value_update(update, context, f'{message}%', method_name, index)
            return CHANGE_PARAM
        else:
            raise ValueError('Value is not from 1-100%')
    except ValueError as e:
        update.message.reply_text(f'Wrong format! {e}')
        logger.warning(f'Value error: {e}: {message}')
        return BATTERY


def background(update, context):
    method_name = 'Background'
    index = (0, 2)
    message = update.message.text
    try:
        if message:
            method_value_update(update, context, message, method_name, index)
            return CHANGE_PARAM
        else:
            raise ValueError('No URL attached')
    except ValueError as e:
        update.message.reply_text(f'Wrong format! {e}')
        logger.warning(f'Value error: {e}: {message}')
        return BACKGROUND


def name(update, context):
    method_name = 'Name'
    index = (1, 0)
    message = update.message.text
    try:
        if message:
            method_value_update(update, context, message, method_name, index)
            message_sender_keyboard[0][0] = message
            return CHANGE_PARAM
        else:
            raise ValueError('Message empty')
    except ValueError as e:
        update.message.reply_text(f'Wrong format! {e}')
        logger.warning(f'Value error: {e}: {message}')
        return NAME


def last_online(update, context):
    method_name = 'Last'
    index = (1, 1)
    message = update.message.text
    try:
        if 'M' in message:
            update.message.reply_text('Enter minutes')
            return LAST_ONLINE_MINUTES
        elif 'H' in message:
            update.message.reply_text('Enter hours')
            return LAST_ONLINE_HOURS
        elif 'yesterday' in message:
            update.message.reply_text('Enter time in hh:mm format')
            return LAST_ONLINE_YESTERDAY
        elif 'dd.mm.yy' in message:
            update.message.reply_text('Enter date in dd.mm.yy format')
            return LAST_ONLINE_DATE
        elif message:
            method_value_update(update, context, message, method_name, index)
            return CHANGE_PARAM
        else:
            raise ValueError('Message empty')
    except ValueError as e:
        update.message.reply_text(f'Wrong format! {e}')
        logger.warning(f'Value error: {e}: {message}')
        return LAST_ONLINE


def last_online_minutes(update, context):
    method_name = 'Last'
    index = (1, 1)
    message = update.message.text
    try:
        if not message.isdigit():
            raise ValueError('Minutes are not digits')
        if 1 <= int(message) <= 59:
            method_value_update(update, context, f'last seen {message} minutes ago', method_name,
                                index)
            return CHANGE_PARAM
        else:
            raise ValueError('Value is not from 1-59')
    except ValueError as e:
        update.message.reply_text(f'Wrong format! {e}')
        logger.warning(f'Value error: {e}: {message}')
        return LAST_ONLINE_MINUTES


def last_online_hours(update, context):
    method_name = 'Last'
    index = (1, 1)
    message = update.message.text
    try:
        if not message.isdigit():
            raise ValueError('Hours are not digits')
        if 1 <= int(message) <= 59:
            method_value_update(update, context, f'last seen {message} hours ago', method_name,
                                index)
            return CHANGE_PARAM
        else:
            raise ValueError('Value is not from 1-59')
    except ValueError as e:
        update.message.reply_text(f'Wrong format! {e}')
        logger.warning(f'Value error: {e}: {message}')
        return LAST_ONLINE_HOURS


def last_online_yesterday(update, context):
    method_name = 'Last'
    index = (1, 1)
    message = update.message.text
    try:
        if ':' in message:
            hh, mm = message.split(':')
        else:
            raise ValueError('":" missing')
        if not (hh.isdigit() and mm.isdigit()):
            raise ValueError('Time is not digits')
        if 1 <= len(hh) <= 2 and 0 <= int(hh) < 24 and len(mm) == 2 and 0 <= int(mm) < 60:
            if len(hh) == 1:
                hh = '0' + hh
            method_value_update(update, context, f'last seen yesterday at {hh}:{mm}', method_name,
                                index)
            return CHANGE_PARAM
        else:
            raise ValueError('There are only 24 hours in the day, try again')
    except ValueError as e:
        update.message.reply_text(f'Wrong format! {e}')
        logger.warning(f'Value error: {e}: {message}')
        return LAST_ONLINE_YESTERDAY


def last_online_date(update, context):
    method_name = 'Last'
    index = (1, 1)
    message = update.message.text
    try:
        if message.count('.') == 2:
            dd, mm, yy = message.split('.')
        else:
            raise ValueError('"." missing')
        if not ((dd.isdigit() and mm.isdigit()) and yy.isdigit()):
            raise ValueError('Time is not digits')
        # Not taking specific months into account
        if len(dd) == 2 and 1 <= int(dd) <= 31 and len(mm) == 2 and 1 <= int(mm) <= 12 \
                and len(yy) == 2:
            method_value_update(update, context, f'last seen {dd}.{mm}.{yy}', method_name, index)
            return CHANGE_PARAM
        else:
            raise ValueError(
                'There are only 30, 31 days in a month and 12 months in a year, try again')
    except ValueError as e:
        update.message.reply_text(f'Wrong format! {e}')
        logger.warning(f'Value error: {e}: {message}')
        return LAST_ONLINE_DATE


def avatar(update, context):
    method_name = 'Avatar'
    index = (1, 2)
    message = update.message.text

    if message:
        method_value_update(update, context, message, method_name, index)
        return CHANGE_PARAM
    else:
        update.message.reply_text('Wrong format, try again')
        return method_name


def add_message(update, context):
    context.user_data['message_count'] += 1
    context.user_data[f'message_{context.user_data["message_count"]}_text'] = update.message.text
    update.message.reply_text('Please estimate how many lines the message will take\n\n'
                              'You can try sending it here first (Not implemented yet, but it will '
                              'work by just telling you message isn\'t digits)')
    return ADD_MESSAGE_LINES


def add_message_lines(update, context):
    message = update.message.text
    try:
        if not message.isdigit():
            raise ValueError('Number is not digits')
        if 1 <= int(message) <= 14:
            context.user_data[f'message_{context.user_data["message_count"]}_lines'] = int(message)
            # update.message.reply_text('Specify when the message was sent (hh:mm)
            # \n\n/skip to set the time specified in \'Time\' parameter')
            update.message.reply_text('Specify when the message was sent (hh:mm)')
            return ADD_MESSAGE_TIME
        else:
            raise ValueError('Value is not from 1-14')
    except ValueError as e:
        update.message.reply_text(f'Wrong format! {e}')
        logger.warning(f'Value error: {e}: {message}')
        return ADD_MESSAGE_LINES


def add_message_time(update, context):
    message = update.message.text
    try:
        if ':' in message:
            hh, mm = message.split(':')
        else:
            raise ValueError('":" missing')
        if not (hh.isdigit() and mm.isdigit()):
            raise ValueError('Time is not digits')
        if 1 <= len(hh) <= 2 and 0 <= int(hh) < 24 and len(mm) == 2 and 0 <= int(mm) < 60:
            if len(hh) == 1:
                hh = '0' + hh
            context.user_data[f'message_{context.user_data["message_count"]}_time'] = f'{hh}:{mm}'
            update.message.reply_text('Choose message sender', reply_markup=message_sender_markup)
            return ADD_MESSAGE_SENDER
        else:
            raise ValueError('There are only 24 hours in the day, try again')
    except ValueError as e:
        update.message.reply_text(f'Wrong format! {e}')
        logger.warning(f'Value error: {e}: {message}')
        return ADD_MESSAGE_TIME


def add_message_sender(update, context):
    message = 'You' if update.message.text == 'You' else 'Interlocutor'
    context.user_data[f'message_{context.user_data["message_count"]}_sender'] = message
    update.message.reply_text('Message added!', reply_markup=createchat_markup)
    return CHANGE_PARAM


def edit_message(update, context):
    return CHANGE_PARAM


def remove_message(update, context):
    return CHANGE_PARAM


def generate(update, context):
    message = update.message.text
    update.message.reply_text('Generating screenshot URL, sit tight')
    URL = screenshot_generation(context.user_data, method_names)
    if message == '.png' or message == '.jpg' or message == '.webp':
        update.message.reply_text(URL + message)
    else:
        update.message.reply_text(URL)
    return CHANGE_PARAM


def presets(update, context):
    update.message.reply_text(
        'Coming soon\n\nHere you can choose pre-configured settings for screenshot creation')


def settings(update, context):
    update.message.reply_text(
        'Coming soon\n\nHere you can configure default settings to change less information '
        'while creating a screenshot')


def cancel(update, context):
    user = update.message.from_user
    logger.info(f"User {user.username} canceled the screenshot creation.")
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    if PROXY:
        REQUEST_KWARGS = {'proxy_url': 'socks5://' + PROXY}
        updater = Updater(TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)
    else:
        updater = Updater(TOKEN, use_context=True)
    create_chat = ConversationHandler(
        entry_points=[CommandHandler('createchat', createchat)],

        states={
            CHANGE_PARAM: [MessageHandler(Filters.text, change_param, pass_user_data=True)],
            TIME: [MessageHandler(Filters.text, time, pass_user_data=True)],
            BATTERY: [MessageHandler(Filters.text, battery, pass_user_data=True)],
            BACKGROUND: [MessageHandler(Filters.text, background, pass_user_data=True)],
            NAME: [MessageHandler(Filters.text, name, pass_user_data=True)],
            LAST_ONLINE: [MessageHandler(Filters.text, last_online, pass_user_data=True)],
            LAST_ONLINE_MINUTES: [
                MessageHandler(Filters.text, last_online_minutes, pass_user_data=True)],
            LAST_ONLINE_HOURS: [
                MessageHandler(Filters.text, last_online_hours, pass_user_data=True)],
            LAST_ONLINE_YESTERDAY: [
                MessageHandler(Filters.text, last_online_yesterday, pass_user_data=True)],
            LAST_ONLINE_DATE: [MessageHandler(Filters.text, last_online_date, pass_user_data=True)],
            AVATAR: [MessageHandler(Filters.text, avatar, pass_user_data=True)],
            ADD_MESSAGE: [MessageHandler(Filters.text, add_message, pass_user_data=True)],
            ADD_MESSAGE_LINES: [
                MessageHandler(Filters.text, add_message_lines, pass_user_data=True)],
            ADD_MESSAGE_TIME: [MessageHandler(Filters.text, add_message_time, pass_user_data=True)],
            ADD_MESSAGE_SENDER: [
                MessageHandler(Filters.text, add_message_sender, pass_user_data=True)],
            EDIT_MESSAGE: [MessageHandler(Filters.text, edit_message, pass_user_data=True)],
            REMOVE_MESSAGE: [MessageHandler(Filters.text, remove_message, pass_user_data=True)],
            GENERATE: [MessageHandler(Filters.text, generate, pass_user_data=True)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', start))
    dp.add_handler(CommandHandler('settings', settings))
    dp.add_handler(create_chat)
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
