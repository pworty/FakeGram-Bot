from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from bot_data import *

reply_keyboard = [['/createchat',],
                  ['/settings']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def start(update, context):
    update.message.reply_text("Hello! I am FakeGram Bot. I can create fake chats screenshots "
                              "with customization of multiple variables on your screen.\n\n"
                              "What I can do:\n"
                              "/createchat - access fake chat screenshot creation menu\n"
                              "/settings - configure default os/time/background/battery",
                              reply_markup=markup)


def createchat(update, context):
    update.message.reply_text('Can\'t do it yet!')


def settings(update, context):
    update.message.reply_text('Can\'t do it yet!')


def main():
    REQUEST_KWARGS = {'proxy_url': 'socks5://' + PROXY}
    updater = Updater(TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("createchat", createchat))
    dp.add_handler(CommandHandler("settings", settings))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
