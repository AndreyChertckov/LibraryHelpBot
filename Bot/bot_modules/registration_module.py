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
    def reg_admin(self, bot, update, args):
        if args and args[0] == open('Bot/key.txt').read():
            self.cntrl.upto_librarian(update.message.chat_id)
            bot.send_message(chat_id=update.message.chat_id, text="You have been update to Librarian",
                             reply_markup=RKM(self.keyboard_dict["admin"], True))
            utils.key_gen()

    # Registration of users
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def registration(self, bot, update):
        chat = update.message.chat_id
        self.is_in_reg[chat] = [0, {"id": chat}]
        bot.send_message(chat_id=chat, text=func_data.sample_messages['reg'])
        bot.send_message(chat_id=chat, text="Enter your name", reply_markup=RKR([[]]))


        # Steps of the registration
        # params:
        #  bot -- This object represents a Bot's commands
        #  update -- This object represents an incoming update

    def reg_steps(self, bot, update):
        chat = update.message.chat_id
        step = self.is_in_reg[chat][0]
        user = self.is_in_reg[chat][1]
        fields = func_data.lists["reg_fields"]

        if step < len(fields):
            text = update.message.text
            user[fields[step]] = text if text != "Faculty (professor, instructor, TA)" else "Faculty"
            step += 1
            self.is_in_reg[chat][0] += 1
            if step < len(fields):
                keyboard = RKM(self.keyboard_dict["status"], True) if fields[step] == "status" else None
                bot.send_message(chat_id=update.message.chat_id, text="Enter your {}".format(fields[step]),
                                 reply_markup=keyboard)
            else:
                text_for_message = func_data.sample_messages['correctness'].format(**user)
                bot.send_message(chat_id=update.message.chat_id, text=text_for_message,
                                 reply_markup=RKM(self.keyboard_dict["reg_confirm"], True))
        elif step == len(fields):
            if update.message.text == "All is correct✅":
                is_incorrect = utils.data_checker(self.is_in_reg[chat][1])
                if is_incorrect[0]:
                    bot.send_message(chat_id=chat, text=is_incorrect[1],
                                     reply_markup=RKM(self.keyboard_dict["unauth"], True))
                else:
                    print(user)
                    self.cntrl.registration(user)
                    self.is_in_reg.pop(chat)
                    bot.send_message(chat_id=chat, text="Your request has been sent.\n Wait for librarian confirmation",
                                     reply_markup=RKM(self.keyboard_dict["unconf"], True))
            elif update.message.text == "Something is incorrect❌":
                self.is_in_reg[chat] = [0, {"id": update.message.chat_id}]
                bot.send_message(chat_id=chat, text="Enter your name", reply_markup=RKR([[]]))

    def confirm(self, bot, update):
        chat = update.message.chat_id
        self.inline_key[chat] = 'conf_flip'
        n = 3
        unconf_users = self.cntrl.get_all_unconfirmed()
        if len(unconf_users) == 0:
            bot.send_message(chat_id=chat, text="There are no application to confirm")
            return
        unconf_users = [unconf_users[i * n:(i + 1) * n] for i in range(len(unconf_users) // n + 1)]
        if not (chat in self.pages):
            self.pages[chat] = 0
        text_message = ("\n" + "-" * 50 + "\n").join(
            ["{}) {} - {}".format(i + 1, user['name'], user["status"]) for i, user in enumerate(unconf_users[0])])
        keyboard = [[IKB(str(i + 1), callback_data=str(i)) for i in range(len(unconf_users[0]))]]
        keyboard += [[IKB("⬅", callback_data='prev'), IKB("➡️", callback_data='next')]]
        update.message.reply_text(text=text_message + "\nCurrent page: " + str(1), reply_markup=IKM(keyboard))

    def conf_flip(self, bot, update):
        query = update.callback_query
        chat = query.message.chat_id
        n = 3
        unconf_users = self.cntrl.get_all_unconfirmed()
        unconf_users = [unconf_users[i * n:(i + 1) * n] for i in range(len(unconf_users) // n + 1)]
        max_page = len(unconf_users) - 1
        if (query.data == "prev" or "next" == query.data) and max_page:
            if query.data == "next":
                if self.pages[chat] == max_page:
                    self.pages[chat] = 0
                else:
                    self.pages[chat] += 1
            if query.data == "prev":
                if self.pages[chat] == 0:
                    self.pages[chat] = max_page
                else:
                    self.pages[chat] -= 1

            text_message = ("\n" + "-" * 50 + "\n").join(
                ["{}) {} - {}".format(i + 1, user['name'], user["status"]) for i, user in
                 enumerate(unconf_users[self.pages[chat]])])
            keyboard = [[IKB(str(i + 1), callback_data=str(i)) for i in range(len(unconf_users[self.pages[chat]]))]]
            keyboard += [[IKB("⬅", callback_data='prev'), IKB("➡️", callback_data='next')]]
            bot.edit_message_text(text=text_message + "\nCurrent page: " + str(self.pages[chat] + 1), chat_id=chat,
                                  message_id=query.message.message_id, reply_markup=IKM(keyboard))
        elif utils.is_int(query.data):
            k = int(query.data)
            user = unconf_users[self.pages[chat]][k]
            text = """
            Check whether all data is correct:\nName: {name}\nAddress: {address}\nPhone: {phone}\nStatus: {status}
            """.format(**user)
            keyboard = [[IKB("Accept✅", callback_data='accept ' + query.data),
                         IKB("Reject️❌", callback_data='reject ' + query.data)]]
            bot.edit_message_text(text=text, chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))
        elif query.data.split(" ")[0] == 'accept':
            k = int(query.data.split(" ")[1])
            user_id = unconf_users[self.pages[chat]][k]["id"]
            self.cntrl.confirm_user(user_id)
            bot.edit_message_text(text="This user was confirmed", chat_id=chat, message_id=query.message.message_id)
            bot.send_message(chat_id=user_id, text="Your application was confirmed",
                             reply_markup=RKM(self.keyboard_dict[self.types[2]], True))
        elif query.data.split(" ")[0] == 'reject':
            k = int(query.data.split(" ")[1])
            user_id = unconf_users[self.pages[chat]][k]["id"]
            self.cntrl.delete_user(user_id)
            bot.edit_message_text(text="This user was rejected", chat_id=chat, message_id=query.message.message_id)
            bot.send_message(chat_id=user_id, text="Your application was rejected",
                             reply_markup=RKM(self.keyboard_dict[self.types[0]], True))

