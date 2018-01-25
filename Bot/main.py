import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent, \
    InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
import logging

token = '537025892:AAHqwqWaGEKdb4bBBQ9CJlKGa8mAqz7fElI'

bot = telegram.Bot(token=token)
updater = Updater(token=token)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    key = telegram.KeyboardButton(text = "test")
    keyboard = [["/start","/books","stop",key]]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard,True)
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!",reply_markup = reply_markup)


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def caps(bot, update):
    # text_caps = ' '.join(args).upper()
    # bot.send_message(chat_id=update.message.chat_id, text=text_caps)
    button_list = [
        InlineKeyboardButton("col1", url="https://vk.com/feed"),
        InlineKeyboardButton("col2", callback_data="2"),
        InlineKeyboardButton("row 2", callback_data="3")
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    bot.send_message(chat_id=update.message.chat_id, text="Blb", reply_markup=reply_markup)


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu
pages = list(list(["book" + str(j) +str(i)] for i in range(5)) for j in range(5))


def books(bot ,update,pages,step = 0):
    if step < 0:
        return
    key = "Книга"
    keyboard = pages[step] + [["<-","->"],["Cancel"]]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    dispatcher.add_handler(CommandHandler('<-', books(bot,update,pages = pages,step = step - 1)))
    dispatcher.add_handler(CommandHandler('->', books(bot,update,pages = pages,step = step + 1)))
    bot.send_message(chat_id=update.message.chat_id, text="My set of books!", reply_markup=reply_markup)


# def inline_caps(bot, update):
#     query = update.inline_query.query
#     if not query:
#         return
#     results = list()
#     results.append(
#         InlineQueryResultArticle(
#             id=query.upper(),
#             title='Caps',
#             input_message_content=InputTextMessageContent(query.upper())
#         )
#     )
#     bot.answer_inline_query(update.inline_query.id, results)
start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)
caps_handler = CommandHandler('caps', caps)
library = CommandHandler("books",books(bot,updater,pages=pages))
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(caps_handler)
dispatcher.add_handler(library)
# dispatcher.add_handler(inline_caps_handler)

updater.start_polling()
updater.idle()
