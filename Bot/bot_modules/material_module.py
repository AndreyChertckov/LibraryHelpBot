import telegram
from telegram import InlineKeyboardMarkup as IKM
from telegram import ReplyKeyboardMarkup as RKM
from telegram import ReplyKeyboardRemove as RKR
from telegram import InlineKeyboardButton as IKB
from telegram.ext import MessageHandler as MHandler
from telegram.ext import Updater, CommandHandler, Filters, CallbackQueryHandler
from Bot.filter import *
from Bot import utils, func_data
import logging
import configs


class Material_module:
    def mat_manage(self, bot, update):
        reply_markup = RKM(self.keyboard_dict["mat_management"], True)
        bot.send_message(chat_id=update.message.chat_id, text="Choose option", reply_markup=reply_markup)

    def add_doc(self, bot, update):
        reply_markup = RKM(self.keyboard_dict["lib_main"], True)
        bot.send_message(chat_id=update.message.chat_id, text="Choose type of material", reply_markup=reply_markup)

    def start_adding(self, bot, update, key):
        chat = update.message.chat_id
        self.is_adding[chat] = [0, {}, key]
        bot.send_message(chat_id=chat, text=func_data.sample_messages[key])
        bot.send_message(chat_id=chat, text="Enter title", reply_markup=RKR([[]]))


    # Steps of the material addition
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def adding_steps(self, bot, update):
        chat = update.message.chat_id
        step = self.is_adding[chat][0]
        doc = self.is_adding[chat][1]
        key = self.is_adding[chat][2]
        fields_bd = func_data.lists[key + "_bd"]
        fields = func_data.lists[key]

        if step < len(fields):
            text = update.message.text
            doc[fields_bd[step]] = int(text) if utils.is_int(text) else text
            step += 1
            self.is_adding[chat][0] += 1
            if step < len(fields):
                bot.send_message(chat_id=update.message.chat_id, text="Enter {}".format(fields[step]))
            else:
                text_for_message = func_data.sample_messages['correctness_' + key].format(**doc)
                bot.send_message(chat_id=update.message.chat_id, text=text_for_message,
                                 reply_markup=RKM(self.keyboard_dict["reg_confirm"], True))
        elif step == len(fields):
            if update.message.text == "All is correct✅":
                self.cntrl.add_document(doc, key)
                self.is_adding.pop(chat)
                bot.send_message(chat_id=chat, text="Document has been added",
                                 reply_markup=RKM(self.keyboard_dict["admin"], True))
            elif update.message.text == "Something is incorrect❌":
                self.is_adding[chat] = [0, {}]
                bot.send_message(chat_id=chat, text="Enter title", reply_markup=RKR([[]]))