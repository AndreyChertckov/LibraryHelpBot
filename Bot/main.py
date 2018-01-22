import telegram
from telegram.ext import Updater, CommandHandler
import logging

token = '537025892:AAHqwqWaGEKdb4bBBQ9CJlKGa8mAqz7fElI'

bot = telegram.Bot(token=token)
updater = Updater(token=token)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()