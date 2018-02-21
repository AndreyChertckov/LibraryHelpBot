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


class User_module:
    def user_manage(self, bot, update):
        keyboard = self.keyboard_dict["user_management"]
        bot.send_message(chat_id=update.message.chat_id, text="Choose option", reply_markup=RKM(keyboard, True))

    def show_users(self, bot, update):
        chat = update.message.chat_id
        self.inline_key[chat] = 'user_flip'
        n = 3
        patrons = self.cntrl.get_all_patrons()
        if len(patrons) == 0:
            bot.send_message(chat_id=chat, text="There are no users")
            return
        patrons = [patrons[i * n:(i + 1) * n] for i in range(len(patrons) // n + 1) if i * n < len(patrons)]
        if not (chat in self.pages):
            self.pages[chat] = 0
        text_message = ("\n" + "-" * 50 + "\n").join(
            ["{}) {} - {}".format(i + 1, user['name'], user["status"]) for i, user in enumerate(patrons[0])])
        keyboard = [[IKB(str(i + 1), callback_data=str(i)) for i in range(len(patrons[0]))]]
        keyboard += [[IKB("⬅", callback_data='prev'), IKB("➡️", callback_data='next')]]
        update.message.reply_text(text=text_message + "\nCurrent page: " + str(1), reply_markup=IKM(keyboard))


    def user_flip(self, bot, update):
        query = update.callback_query
        chat = query.message.chat_id
        n = 3
        patrons = self.cntrl.get_all_patrons()
        patrons = [patrons[i * n:(i + 1) * n] for i in range(len(patrons) // n + 1) if i * n < len(patrons)]
        max_page = len(patrons) - 1
        if (query.data in ["prev", "next", 'cancel']) and (max_page or query.data == 'cancel'):
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
                 enumerate(patrons[self.pages[chat]])])
            keyboard = [[IKB(str(i + 1), callback_data=str(i)) for i in range(len(patrons[self.pages[chat]]))]]
            keyboard += [[IKB("⬅", callback_data='prev'), IKB("➡️", callback_data='next')]]
            bot.edit_message_text(text=text_message + "\nCurrent page: " + str(self.pages[chat] + 1), chat_id=chat,
                                  message_id=query.message.message_id, reply_markup=IKM(keyboard))
        elif utils.is_int(query.data):
            k = int(query.data)
            user = patrons[self.pages[chat]][k]
            text = """
            Name: {name}\nAddress: {address}\nPhone: {phone}\nStatus: {status}\n Current book:{current_books}
            """.format(**user)
            keyboard = [[IKB("Cancel", callback_data='cancel')]]
            bot.edit_message_text(text=text, chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))
