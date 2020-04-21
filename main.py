from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import ConversationHandler, CommandHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from bot_data import *

menu_keyboard = [['/createchat', '/presets'],
                 ['/settings']]
createchat_keyboard = [['Time', 'Battery', 'Background'],
                       ['Name', 'Last online', 'Profile pic'],
                       ['Add message', 'Remove message'],
                       ['Generate']]
keypad = [['1', '2', '3'],
          ['4', '5', '6'],
          ['7', '8', '9'],
          ['', '0', '']]
time_keyboard = [['1', '2', '3'],
                 ['4', '5', '6'],
                 ['7', '8', '9'],
                 [':', '0', ':']]
last_seen_keyboard = [[InlineKeyboardButton('Online')],
                      [InlineKeyboardButton('Last seen recently')],
                      [InlineKeyboardButton('Last seen M minutes ago')],
                      [InlineKeyboardButton('Last seen H hours ago')],
                      [InlineKeyboardButton('Last seen yesterday at hh:mm')],
                      [InlineKeyboardButton('Last seen dd.mm.yy')],
                      [InlineKeyboardButton('Last seen a long time ago')]]

menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False)
createchat_markup = ReplyKeyboardMarkup(createchat_keyboard, one_time_keyboard=True)
keypad_markup = ReplyKeyboardMarkup(keypad, one_time_keyboard=False)
time_markup = ReplyKeyboardMarkup(time_keyboard, one_time_keyboard=False)
last_seen_markup = InlineKeyboardMarkup.from_button(InlineKeyboardButton('Last seen a long time ago'))


def start(update, context):
    update.message.reply_text("Hello! I am FakeGram Bot. I can create fake chats screenshots "
                              "with customization of multiple variables on your screen.\n\n"
                              "What I can do:\n"
                              "/createchat - access fake chat screenshot creation menu\n"
                              "(Right now it resets your settings!)\n"
                              "/presets - use one of the presets to creat a fake chat\n"
                              "/settings - configure default time/background/battery and more",
                              reply_markup=menu_markup)


def stop(update, context):
    return ConversationHandler.END


def createchat(update, context):
    update.message.reply_text('Alright, now configure settings and press \'Generate\' to get the '
                              'screenshot', reply_markup=createchat_markup)
    context.user_data['Time'] = 'Default'
    context.user_data['Battery'] = 'Default'
    context.user_data['Background'] = 'Default'
    context.user_data['Name'] = 'Default'
    context.user_data['Last online'] = 'Default'
    context.user_data['Profile pic'] = 'Default'
    return 'Change param'


def change_param(update, context):
    print(context.user_data)
    message = update.message.text.split()[0]
    if message == 'Time':
        update.message.reply_text('Enter time in hh:mm format')
    elif message == 'Battery':
        update.message.reply_text('Enter battery percentage from 1 to 100 (no % sign)')
    elif message == 'Background':
        update.message.reply_text('')
    elif message == 'Name':
        update.message.reply_text('Enter the user\'s name')
    elif message == 'Last' and update.message.text.split()[1] == 'online':
        update.message.reply_text('Choose one type from options', reply_markup=last_seen_markup)
    elif message == 'Profile pic':
        update.message.reply_text('Send a profile picture')
    return message


def method_value_update(update, context, method_name, index):
    old = context.user_data.get(method_name, 'None')
    new = update.message.text + '%'
    createchat_keyboard[index[0]][index[1]] = f'{method_name} - {new}'
    update.message.reply_text(f'{method_name} updated! ({old} -> {new})',
                              reply_markup=createchat_markup)
    context.user_data[method_name] = new


def time(update, context):
    method_name = 'Battery'
    index = (0, 0)
    message = update.message.text

    hh, mm = message.split(':')
    if hh.isdigit() and mm.isdigit() and 1 <= len(hh) <= 2 and len(mm) == 2:
        method_value_update(update, context, method_name, index)
        return 'Change param'
    else:
        update.message.reply_text('Wrong format, try again')
        return method_name


def battery(update, context):
    method_name = 'Battery'
    index = (0, 1)
    message = update.message.text

    if message.isdigit() and 0 < int(message) <= 100:
        method_value_update(update, context, method_name, index)
        return 'Change param'
    else:
        update.message.reply_text('Wrong format, try again')
        return method_name


def background(update, context):
    method_name = 'Background'
    index = (0, 2)
    message = update.message.text

    if message:
        pass
        return 'Change param'
    else:
        update.message.reply_text('Wrong format, try again')
        return method_name


def name(update, context):
    method_name = 'Name'
    index = (1, 0)
    message = update.message.text

    method_value_update(update, context, method_name, index)
    return 'Change param'


def last_online(update, context):
    method_name = 'Last online'
    index = (1, 1)
    message = update.message.text

    if message:
        pass
        return 'Change param'
    else:
        update.message.reply_text('Wrong format, try again')
        return method_name


def profile_pic(update, context):
    method_name = 'Profile pic'
    index = (1, 2)
    message = update.message.text

    if message:
        pass
        return 'Change param'
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


def VPN(state):
    if state == 'ON':
        pass


def main():
    if PROXY:
        REQUEST_KWARGS = {'proxy_url': 'socks5://' + PROXY}
        updater = Updater(TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)
    else:
        updater = Updater(TOKEN, use_context=True)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('createchat', createchat)],

        states={
            'Change param': [MessageHandler(Filters.text, change_param, pass_user_data=True)],
            'Time': [MessageHandler(Filters.text, time, pass_user_data=True)],
            'Battery': [MessageHandler(Filters.text, battery, pass_user_data=True)],
            'Background': [MessageHandler(Filters.text, background, pass_user_data=True)],
            'Name': [MessageHandler(Filters.text, name, pass_user_data=True)],
            'Last online': [MessageHandler(Filters.text, last_online, pass_user_data=True)],
            'Profile pic': [MessageHandler(Filters.text, profile_pic, pass_user_data=True)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', start))
    dp.add_handler(CommandHandler('settings', settings))
    dp.add_handler(conv_handler)
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
