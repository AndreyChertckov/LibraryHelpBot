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


class Reg_module:

    # Registration of admins
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    #  args -- Arguments
    def upto_admin(self, bot, update, args):
        if args and args[0] == open('Bot/key.txt').read():
            self.controller.upto_librarian(update.message.chat_id)
            bot.send_message(chat_id=update.message.chat_id, text="You have been update to Librarian",
                             reply_markup=RKM(self.keyboard_dict["admin"], True))
            utils.key_gen()

    # Registration of users
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def registration(self, bot, update):
        # self.location = {}
        chat = update.message.chat_id
        self.location[chat] = 'reg'
        self.user_data[chat] = [0, {"id": chat}]
        bot.send_message(chat_id=chat, text=func_data.sample_messages['reg'])
        bot.send_message(chat_id=chat, text="Enter your name", reply_markup=RKR([[]]))

    # Steps of the registration
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def reg_steps(self, bot, update):
        chat = update.message.chat_id
        step, user = self.user_data[chat]
        fields = func_data.lists["reg_fields"]

        if step < len(fields):
            text = update.message.text
            user[fields[step]] = text if text != "Faculty (professor, instructor, TA)" else "Faculty"
            step += 1
            self.user_data[chat][0] += 1
            if step < len(fields):
                keyboard = RKM(self.keyboard_dict["status"], True) if fields[step] == "status" else None
                bot.send_message(chat_id=update.message.chat_id, text="Enter your {}".format(fields[step]),
                                 reply_markup=keyboard)
            else:
                text_for_message = func_data.sample_messages['correctness'].format(**user)
                bot.send_message(chat_id=chat, text=text_for_message,
                                 reply_markup=RKM(self.keyboard_dict["reg_confirm"], True))
        elif step == len(fields):
            if update.message.text == "All is correct✅":
                is_incorrect = utils.data_checker(self.user_data[chat][1])
                if is_incorrect[0]:
                    bot.send_message(chat_id=chat, text=is_incorrect[1],
                                     reply_markup=RKM(self.keyboard_dict["unauth"], True))
                else:
                    self.controller.registration(user)
                    bot.send_message(chat_id=chat, text="Your request has been sent.\n Wait for librarian confirmation",
                                     reply_markup=RKM(self.keyboard_dict["unconf"], True))
                    self.main_menu(bot, update)
            elif update.message.text == "Something is incorrect❌":
                self.user_data[chat] = [0, {"id": chat}]
                bot.send_message(chat_id=chat, text="Enter your name", reply_markup=RKR([[]]))

    def confirm(self, bot, update):
        self.location[update.message.chat_id] = 'confirm'
        self.online_init(bot, update)

    def conf_user(self, bot, ids, user_id, action):
        if action == 'accept':
            self.controller.confirm_user(user_id)
            bot.edit_message_text(text="This user was confirmed", chat_id=ids[0], message_id=ids[1])
            bot.send_message(chat_id=user_id, text="Your application was confirmed",
                             reply_markup=RKM(self.keyboard_dict[self.types[2]], True))
        elif action == 'reject':
            self.controller.delete_user(user_id)
            bot.edit_message_text(text="This user was rejected", chat_id=ids[0], message_id=ids[1])
            bot.send_message(chat_id=user_id, text="Your application was rejected",
                             reply_markup=RKM(self.keyboard_dict[self.types[0]], True))

