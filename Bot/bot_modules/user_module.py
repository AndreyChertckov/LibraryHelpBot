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
        bot.send_message(chat_id=update.message.chat_id, text="Choose option", reply_markup=RKM(keyboard, True))

    def show_users(self, bot, update):
        self.pages = {}
        chat = update.message.chat_id
        self.inline_key[chat] = 'user_flip'
        n = 3
        patrons = self.cntrl.get_all_patrons()
        if len(patrons) == 0:
            bot.send_message(chat_id=chat, text="There are no users")
            return
        patrons = [patrons[i * n:(i + 1) * n] for i in range(len(patrons) // n + 1) if i * n < len(patrons)]
        if not (chat in self.pages):
            self.pages[chat] = [0, 0, []]
        text_message = ("\n" + "-" * 50 + "\n").join(
            ["{}) {} - {}".format(i + 1, user['name'], user["status"]) for i, user in enumerate(patrons[0])])
        keyboard = [[IKB(str(i + 1), callback_data=str(i)) for i in range(len(patrons[0]))]]
        keyboard += [[IKB("⬅", callback_data='prev'), IKB("➡️", callback_data='next')]]
        update.message.reply_text(text=text_message + "\n\nCurrent page: 1/{}".format(len(patrons)),
                                  reply_markup=IKM(keyboard))

    def user_flip(self, bot, update):
        query = update.callback_query
        chat = query.message.chat_id
        n = 3
        k = self.pages[chat][1]
        patrons = self.cntrl.get_all_patrons()
        patrons = [patrons[i * n:(i + 1) * n] for i in range(len(patrons) // n + 1) if i * n < len(patrons)]
        user = patrons[self.pages[chat][0]][k]
        user_id = user['id']
        max_page = len(patrons) - 1
        if (query.data in ["prev", "next", 'cancel']) and (max_page or query.data == 'cancel'):
            self.location.pop(chat, 0)
            self.pages[chat][2] = 0
            if query.data == "next":
                if self.pages[chat][0] == max_page:
                    self.pages[chat][0] = 0
                else:
                    self.pages[chat][0] += 1
            if query.data == "prev":
                if self.pages[chat][0] == 0:
                    self.pages[chat][0] = max_page
                else:
                    self.pages[chat][0] -= 1

            text_message = ("\n" + "-" * 50 + "\n").join(
                ["{}) {} - {}".format(i + 1, user['name'], user["status"]) for i, user in
                 enumerate(patrons[self.pages[chat][0]])])
            keyboard = [[IKB(str(i + 1), callback_data=str(i)) for i in range(len(patrons[self.pages[chat][0]]))]]
            keyboard += [[IKB("⬅", callback_data='prev'), IKB("➡️", callback_data='next')]]
            bot.edit_message_text(
                text=text_message + "\n\nCurrent page: {}/{}".format(self.pages[chat][0] + 1, len(patrons)),
                chat_id=chat,
                message_id=query.message.message_id, reply_markup=IKM(keyboard))
        elif utils.is_int(query.data):
            k = int(query.data)
            self.pages[chat][1] = k
            user = patrons[self.pages[chat][0]][k]
            user_id = user['id']
            orders = self.cntrl.get_user_orders(user_id)
            text = """
            Name: {name}\nAddress: {address}\nPhone: {phone}\nStatus: {status}\nTaken documents: """.format(**user)
            text += "{}\nOverdue documents: ".format(len(orders))
            text += str(len([i for i in orders if datetime.strptime(i['time_out'], "%Y-%m-%d") < datetime.today()]))
            keyboard = [[IKB("Edit", callback_data='edit'), IKB("Cancel", callback_data='cancel')]]
            if orders:
                keyboard[0].insert(1, IKB("Orders", callback_data='order'))
            else:
                keyboard[0].insert(1, IKB("Delete", callback_data='delete'))
            bot.edit_message_text(text=text, chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))
        elif query.data == 'order':
            orders = self.cntrl.get_user_orders(user_id)
            # print(orders)
            keyboard = [[IKB(str(i + 1), callback_data='order ' + str(i)) for i in range(len(orders))]]
            self.pages[chat][2] = orders
            orders = ("\n" + "-" * 50 + "\n").join(
                ["{}) {} written by {}\n Available till {}".format(i + 1, doc['doc_dict']['title'],
                                                                   doc['doc_dict']['authors'], doc['time_out']) for
                 i, doc in
                 enumerate(orders)])
            keyboard += [[IKB("Cancel", callback_data='cancel')]]
            bot.edit_message_text(text=orders, chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))
        elif query.data == 'edit':
            keyboard = [[IKB("Name", callback_data='e1'), IKB("Phone", callback_data='e3')],
                        [IKB("Address", callback_data='e2'), IKB("Status", callback_data='e4')],
                        [IKB("Cancel", callback_data='cancel')]]
            text = "Choose edited parameter or press cancel"
            bot.edit_message_text(text=text, chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))
        elif query.data == 'delete':
            self.cntrl.delete_user(user_id)
            text = "User card has been deleted"
            bot.edit_message_text(text=text, chat_id=chat, message_id=query.message.message_id)
        elif query.data in ['e1', 'e2', 'e3', 'e4']:
            keyboard = [[IKB("Cancel", callback_data='cancel')]]
            params = dict(zip(['e1', 'e2', 'e3', 'e4'], func_data.lists["reg_fields"]))
            text = 'Enter new {}.\nOld value - {}.'.format(params[query.data], user[params[query.data]])
            self.location[chat] = ["user_modify", user, params[query.data]]
            bot.edit_message_text(text=text, chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))
        elif query.data.split(" ")[0] == 'order' and utils.is_int(query.data.split(" ")[1]):
            # print(self.pages[chat][2])
            self.location[chat] = ["notice", user_id]
            doc, time, time_out = self.pages[chat][2][int(query.data.split(" ")[1])].values()
            text = "User name: {name}\nPhone: {phone}\nStatus: {status}\n\n".format(**user)
            text += "Document title: {title}\nAuthors: {authors}\n\n".format(**doc)
            text += "Date of taking: {}\nDate of returning: {}".format(time, time_out)
            keyboard = [[IKB("Book return", callback_data='return'),
                         IKB("Send notification", callback_data='notice'),
                         IKB("Cancel", callback_data='cancel')]]
            bot.edit_message_text(text=text, chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))
        elif query.data == 'notice':
            keyboard = [[IKB("Cancel", callback_data='cancel')]]
            text = "Enter message to user"
            bot.edit_message_text(text=text, chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))
        elif query.data == 'return':
            doc, time, time_out = self.pages[chat][2][int(query.data.split(" ")[1])].values()
            self.cntrl.return_doc(doc)
            keyboard = [[IKB("Return to the list", callback_data='cancel')]]

            bot.edit_message_text(text='Document was returned', chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))

    def modify_user(self, bot, update):
        chat = update.message.chat_id
        user, parametr = self.location[chat][1:]
        user[parametr] = update.message.text
        self.cntrl.modify_user(user)
        self.location.pop(chat, 0)
        bot.send_message(text='User data was updated', chat_id=chat)

    def notice_user(self, bot, update):
        chat = update.message.chat_id
        user_id = self.location[chat][1]
        self.location.pop(chat, 0)
        bot.send_message(text=update.message.text, chat_id=user_id)
        bot.send_message(text='Message sent', chat_id=chat)
