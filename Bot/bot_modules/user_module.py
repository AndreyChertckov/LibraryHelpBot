import telegram
from telegram import InlineKeyboardMarkup as IKM
from telegram import ReplyKeyboardMarkup as RKM
from telegram import ReplyKeyboardRemove as RKR
from telegram import InlineKeyboardButton as IKB
from telegram.ext import MessageHandler as MHandler
from telegram.ext import Updater, CommandHandler, Filters, CallbackQueryHandler
from Bot.filter import *
from Bot import utils, func_data
from datetime import datetime
import logging
import configs


class User_module:
    def user_manage(self, bot, update):
        keyboard = self.keyboard_dict["user_management"]
        self.location[update.message.chat_id] = 'user_management'
        bot.send_message(chat_id=update.message.chat_id, text="Choose option", reply_markup=RKM(keyboard, True))

    def show_users(self, bot, update):
        self.location[update.message.chat_id] = 'users'
        self.online_init(bot, update)

