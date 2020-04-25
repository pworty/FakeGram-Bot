import logging

from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import ConversationHandler, CommandHandler
from telegram import ReplyKeyboardRemove

from bot_data import TOKEN, PROXY
from keyboards import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHANGE_PARAM, TIME, BATTERY, BACKGROUND, NAME, LAST_ONLINE, PROFILE_PIC = range(7)
method_names = {'Time': 1, 'Battery': 2, 'Background': 3, 'Name': 4, 'Last': 5, 'Profile': 6}


def start(update, context):
    update.message.reply_text("Hello! I am FakeGram Bot. I can create fake chats screenshots "
                              "with customization of multiple variables on your screen.\n\n"
                              "What I can do:\n"
                              "/createchat - access fake chat screenshot creation menu\n"
                              "(Right now it resets your settings!)\n"
                              "/presets - use one of the presets to creat a fake chat\n"
                              "/settings - configure default time/background/battery and more",
                              reply_markup=menu_markup)


def createchat(update, context):
    update.message.reply_text('Alright, now configure settings and press \'Generate\' to get the '
                              'screenshot\n\n'
                              '/cancel to stop screenshot creation. Changes will not be saved!',
                              reply_markup=createchat_markup)
    context.user_data[TIME] = '09:41'
    context.user_data[BATTERY] = '100%'
    context.user_data[BACKGROUND] = 'Default'
    context.user_data[NAME] = 'Lucinda Lane'
    context.user_data[LAST_ONLINE] = 'last seen 5 minutes ago'
    context.user_data[PROFILE_PIC] = 'Default'
    return CHANGE_PARAM


def change_param(update, context):
    print(context.user_data)
    message = update.message.text.split()[0]
    if message == 'Time':
        update.message.reply_text('Enter time in "hh:mm" format')
    if message == 'Battery':
        update.message.reply_text('Enter battery percentage from 1 to 100 (no % sign)')
    if message == 'Background':
        update.message.reply_text('')
    if message == 'Name':
        update.message.reply_text('Enter the user\'s name')
    if message == 'Last' and update.message.text.split()[1] == 'online':
        update.message.reply_text('Choose one type from options', reply_markup=last_seen_markup)
    if message == 'Profile':
        update.message.reply_text('Send a profile picture')
    if message == '/cancel':
        update.message.reply_text('Stopping screenshot creation', reply_markup=menu_markup)
    return method_names.get(message, message)


def method_value_update(update, context, new, method_name, index):
    old = context.user_data.get(method_name, 'None')
    createchat_keyboard[index[0]][index[1]] = f'{method_name} - {new}'
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


def background(update, context):
    method_name = 'Background'
    index = (0, 2)
    message = update.message.text

    if message:
        pass
        return CHANGE_PARAM
    else:
        update.message.reply_text('Wrong format, try again')
        return BACKGROUND


def name(update, context):
    method_name = 'Name'
    index = (1, 0)
    method_value_update(update, context, update.message.text, method_name, index)
    return CHANGE_PARAM


def last_online(update, context):
    method_name = 'Last online'
    index = (1, 1)
    message = update.message.text

    if message:
        pass
        return CHANGE_PARAM
    else:
        update.message.reply_text('Wrong format, try again')
        return method_name


def profile_pic(update, context):
    method_name = 'Profile pic'
    index = (1, 2)
    message = update.message.text

    if message:
        pass
        return CHANGE_PARAM
    else:
        update.message.reply_text('Wrong format, try again')
        return method_name


def add_message(update, context):
    pass


def remove_message(update, context):
    pass


def generate(update, context):
    pass


def settings(update, context):
    update.message.reply_text('Here you can configure default settings to change less information '
                              'while creating a screenshot')


def cancel(update, context):
    # user = update.message.from_user
    # logger.info(f"User {user.username} canceled the screenshot creation.")
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
            PROFILE_PIC: [MessageHandler(Filters.text, profile_pic, pass_user_data=True)]
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
