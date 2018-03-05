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
        self.location[update.message.chat_id] = 'material_management'
        bot.send_message(chat_id=update.message.chat_id, text="Choose option", reply_markup=reply_markup)

    def add_doc(self, bot, update):
        self.location[update.message.chat_id] = "add_doc"
        reply_markup = RKM(self.keyboard_dict["lib_main"], True)
        bot.send_message(chat_id=update.message.chat_id, text="Choose type of material", reply_markup=reply_markup)

    def start_adding(self, bot, update):
        key = func_data.analog[update.message.text]
        chat = update.message.chat_id
        self.location[chat] = "add_doc"
        self.user_data[chat] = [0, {}, key]
        bot.send_message(chat_id=chat, text=func_data.sample_messages[key])
        bot.send_message(chat_id=chat, text="Enter title", reply_markup=RKR([[]]))

    # Steps of the material addition
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def adding_steps(self, bot, update):
        chat = update.message.chat_id
        step = self.user_data[chat][0]
        doc = self.user_data[chat][1]
        key = self.user_data[chat][2]
        fields_bd = func_data.lists[key + "_bd"]
        fields = func_data.lists[key]

        if step < len(fields):
            text = update.message.text
            doc[fields_bd[step]] = int(text) if utils.is_int(text) else text
            step += 1
            self.user_data[chat][0] += 1
            if step < len(fields):
                bot.send_message(chat_id=chat, text="Enter {}".format(fields[step]))
            else:
                text = func_data.sample_messages['correctness_' + key].format(**doc)
                bot.send_message(chat_id=chat, text=text, reply_markup=RKM(self.keyboard_dict["reg_confirm"], True))
        elif step == len(fields):
            if update.message.text == "All is correct✅":
                self.controller.add_document(doc, key)
                self.location[chat] = 'main'
                bot.send_message(chat_id=chat, text="Document has been added",
                                 reply_markup=RKM(self.keyboard_dict["admin"], True))
            elif update.message.text == "Something is incorrect❌":
                self.user_data[chat] = [0, {}, key]
                bot.send_message(chat_id=chat, text="Enter title", reply_markup=RKR([[]]))

    # Main menu of library
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def library(self, bot, update):
        self.location[update.message.chat_id] = 'library'
        bot.send_message(chat_id=update.message.chat_id, text="Choose type of material",
                         reply_markup=RKM(self.keyboard_dict["lib_main"], True))

    # Selected material
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def load_material(self, bot, update):
        self.location[update.message.chat_id] = 'library'
        self.online_init(bot, update)

    def modify_document(self, bot, ids, action, args):
        chat, message_id = ids
        if action == 'order':
            doc_id, doc_type = args
            status, report = self.controller.check_out_doc(chat, int(doc_id), type_bd=doc_type)
            message = "Your order was successful.\nYou may take the document during library working hours." if status else "You already have this document"
            bot.edit_message_text(text=message, chat_id=chat, message_id=message_id)
        elif action == 'del':
            message = "Are you sure want to delete this document?"
            markup = IKM([[IKB('Yes', callback_data='yes {} library'.format(args[1])),
                           IKB('No', callback_data='cancel {} {} library'.format(args[0], args[-1]))]])
            bot.edit_message_text(chat_id=chat, message_id=message_id, text=message, reply_markup=markup)
        elif action == 'yes':
            message = 'Document was deleted successfully'
            self.controller.delete_document(*args[1:])
            bot.edit_message_text(text=message, chat_id=chat, message_id=message_id)
        elif action == 'edit':
            doc_type = args[-1]
            callback = ['e{} {} {} {} library'.format(i, *args) for i in range(9)]
            keyboard = [[IKB("Title", callback_data=callback[0]), IKB("Author", callback_data=callback[1])]]
            if doc_type == 'book':
                keyboard += [
                    [IKB("Description", callback_data=callback[2]), IKB("Keywords", callback_data=callback[3])],
                    [IKB("Price", callback_data=callback[4]), IKB("Count", callback_data=callback[5])]]
            elif doc_type == 'article':
                keyboard += [[IKB("Journal", callback_data=callback[2]), IKB("Issue", callback_data=callback[3])],
                             [IKB("Editors", callback_data=callback[4]), IKB("Date", callback_data=callback[5])],
                             [IKB("Keywords", callback_data=callback[6]), IKB("Price", callback_data=callback[7])],
                             IKB("Count", callback_data=callback[8])]
            elif doc_type == 'media':
                keyboard += [[IKB("Keywords", callback_data=callback[2]), [IKB("Price", callback_data=callback[3])],
                              IKB("Count", callback_data=callback[4])]]
            keyboard += [[IKB('Cancel️', callback_data='cancel {} {} library'.format(args[0], args[-1]))]]
            text = "Choose edited parameter"
            bot.edit_message_text(text=text, chat_id=chat, message_id=message_id,
                                  reply_markup=IKM(keyboard))
        elif action in ['e{}'.format(i) for i in range(9)]:
            doc_type = args[-1]
            doc_id = args[1]
            parameter = func_data.lists[doc_type][int(action[1])]
            parameter_db = func_data.lists[doc_type + "_bd"][int(action[1])]
            doc = self.controller.get_document(doc_id, doc_type)
            keyboard = [[IKB('Cancel️', callback_data='cancel {} {} library'.format(args[0], args[-1]))]]
            text = 'Enter new {}.\nOld value - {}.'.format(parameter, doc[parameter_db])
            self.location[chat] = "doc_modify"
            self.user_data[chat] = [doc, parameter_db, doc_type]
            bot.edit_message_text(text=text, chat_id=chat, message_id=message_id, reply_markup=IKM(keyboard))

    def update_doc_param(self, bot, update):
        chat = update.message.chat_id
        doc, parameter, doc_type = self.user_data[chat]
        doc[parameter] = update.message.text
        self.controller.update_doc_param(doc, doc_type)
        self.location[chat] = 'library'
        bot.send_message(text='Document was updated', chat_id=chat)

    def user_orders(self, bot, update):
        self.location[update.message.chat_id] = 'my_orders'
        self.online_init(bot, update)
