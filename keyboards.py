from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

# Keyboards
# menu_keyboard = [['/createchat', '/presets'], ['/settings', '/help']]

menu_keyboard = [['/createchat']]

createchat_keyboard = [['Time', 'Battery', 'Background'],
                       ['Name', 'Last online', 'Avatar'],
                       ['Add message', 'Edit message', 'Remove message'],
                       ['Generate']]

settings_keyboard = [['Time', 'Battery', 'Background'],
                     ['Name', 'Last online', 'Avatar']]

last_seen_keyboard = [['online'],
                      ['last seen recently'],
                      ['last seen M minutes ago'],
                      ['last seen H hours ago'],
                      ['last seen yesterday at hh:mm'],
                      ['last seen dd.mm.yy'],
                      ['last seen a long time ago']]

image_format_keyboard = [['.png'],
                         ['.jpg'],
                         ['.webp']]

message_sender_keyboard = [['Interlocutor', 'You']]

# Keyboard markups
menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False)
createchat_markup = ReplyKeyboardMarkup(createchat_keyboard, one_time_keyboard=True)
settings_markup = ReplyKeyboardMarkup(settings_keyboard, one_time_keyboard=False)

last_seen_markup = ReplyKeyboardMarkup(last_seen_keyboard)
image_format_markup = ReplyKeyboardMarkup(image_format_keyboard, one_time_keyboard=True)
message_sender_markup = ReplyKeyboardMarkup(message_sender_keyboard, one_time_keyboard=True)
