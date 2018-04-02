import telegram
from telegram import InlineKeyboardMarkup as IKM
from telegram import ReplyKeyboardMarkup as RKM
from telegram import ReplyKeyboardRemove as RKR
from telegram import InlineKeyboardButton as IKB
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

    def user_flip(self, bot, ids, action, args):
        chat, message_id = ids
        user_id = args[1]
        if action == 'orders':
            orders = self.controller.get_user_orders(user_id)
            keyboard = [
                [IKB(str(i + 1), callback_data='order {} {} {} users'.format(*args, i)) for i in range(len(orders))]]
            orders = func_data.text_gen(orders, "orders")
            keyboard += [[IKB('Cancel️', callback_data='cancel {} {} users'.format(*args))]]
            bot.edit_message_text(text=orders, chat_id=chat, message_id=message_id, reply_markup=IKM(keyboard))
        elif action == 'edit':
            callback = ['e{} {} {} users'.format(i, *args) for i in range(4)]
            keyboard = [[IKB("Name", callback_data=callback[0]), IKB("Phone", callback_data=callback[1])],
                        [IKB("Address", callback_data=callback[2]), IKB("Status", callback_data=callback[3])],
                        [IKB('Cancel️', callback_data='cancel {} {} users'.format(*args))]]
            text = "Choose edited parameter or press cancel"
            bot.edit_message_text(text=text, chat_id=chat, message_id=message_id, reply_markup=IKM(keyboard))
        elif action == 'delete':
            self.controller.delete_user(user_id)
            text = "User card has been deleted"
            bot.edit_message_text(text=text, chat_id=chat, message_id=message_id)
            bot.send_message(text="Your user card was deleted.", chat_id=user_id,
                             reply_markup=RKM(self.keyboard_dict['unauth'], True))
        elif action in ['e0', 'e1', 'e2', 'e3']:
            user = self.controller.get_user(user_id)
            keyboard = [[IKB("Cancel", callback_data='cancel {} {} users'.format(*args))]]
            params = dict(zip(['e0', 'e1', 'e2', 'e3'], func_data.lists["reg_fields"]))
            text = 'Enter new {}.\nOld value - {}.'.format(params[action], user[params[action]])
            self.location[chat] = "user_modify"
            self.user_data[chat] = [user, params[action]]
            bot.edit_message_text(text=text, chat_id=chat, message_id=message_id, reply_markup=IKM(keyboard))
        elif action == 'order':
            self.user_data[chat] = user_id
            user = self.controller.get_user(user_id)
            order = self.controller.get_user_orders(user_id)[int(args[-1])]
            doc, order_id, active = order['doc'], order['id'], order['active']
            doc_type, time, time_out = order['table'], order['time'], order['time_out']

            text = "User name: {name}\nPhone: {phone}\nStatus: {status}\n\n".format(**user)
            text += "Document title: {title}\nAuthors: {authors}\nType of document: {dt}\n\n".format(**doc, dt=doc_type)
            text += "Date of taking: {}\nDate of returning: {}".format(time, time_out)

            if int(active) == 0:
                keyboard = [[IKB("Activate order", callback_data='activate {} {} {} users'.format(*args)),
                             IKB("Decline order", callback_data='decline {} {} {} users'.format(*args)),
                             IKB('Cancel️', callback_data='cancel {} {} users'.format(*args[:-1]))]]
            elif int(active) == 1:
                keyboard = [[IKB("Book return", callback_data='return {} {} {} users'.format(*args)),
                             IKB("Send notification", callback_data='notice {} {} {} users'.format(*args)),
                             IKB('Cancel️', callback_data='cancel {} {} users'.format(*args[:-1]))]]
            bot.edit_message_text(text=text, chat_id=chat, message_id=message_id, reply_markup=IKM(keyboard))
        elif action == 'activate':
            order = self.controller.get_user_orders(user_id)[int(args[-1])]
            self.controller.user_get_doc(order['id'])
            keyboard = [[IKB("Return to the list", callback_data='cancel {} {} users'.format(*args))]]

            bot.edit_message_text(text='Document was taken', chat_id=chat, message_id=message_id,
                                  reply_markup=IKM(keyboard))
        elif action == 'decline':
            order = self.controller.get_user_orders(user_id)[int(args[-1])]
            self.controller.return_doc(order['id'])
            keyboard = [[IKB("Return to the list", callback_data='cancel {} {} users'.format(*args))]]
            bot.edit_message_text(text='Order was declined', chat_id=chat, message_id=message_id,
                                  reply_markup=IKM(keyboard))
        elif action == 'notice':
            self.location[chat] = "notice"
            keyboard = [[IKB('Cancel️', callback_data='cancel {} {} users'.format(*args))]]
            text = "Enter message to user"
            bot.edit_message_text(text=text, chat_id=chat, message_id=message_id, reply_markup=IKM(keyboard))
        elif action == 'return':
            order = self.controller.get_user_orders(user_id)[int(args[-1])]
            result = self.controller.return_doc(order['id'])
            if result[0]:
                if result[1] != 0:
                    bot.send_message(text="Please pay fine, because you returned it late : {}".format(result[1]),
                                     chat_id=user_id)
                    text = "User have fine: {}".format(result[1])
                else:
                    bot.send_message(text="Book was returned.Thank you, that you use our service", chat_id=user_id)
                    text = "User have not fine"
            text = 'Document was returned.' + text
            keyboard = [[IKB("Return to the list", callback_data='cancel {} {} users'.format(*args))]]
            bot.edit_message_text(text=text, chat_id=chat, message_id=message_id, reply_markup=IKM(keyboard))

    def modify_user(self, bot, update):
        chat = update.message.chat_id
        user, parameter = self.user_data[chat]
        user[parameter] = update.message.text
        self.controller.modify_user(user)
        self.location[chat] = 'users'
        bot.send_message(text='User data was updated', chat_id=chat)

    def notice_user(self, bot, update):
        chat = update.message.chat_id
        user_id = self.user_data[chat]
        self.location[chat] = 'users'
        bot.send_message(text=update.message.text, chat_id=user_id)
        bot.send_message(text='Message sent', chat_id=chat)
