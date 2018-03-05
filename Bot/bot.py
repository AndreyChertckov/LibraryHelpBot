import telegram
from telegram import InlineKeyboardMarkup as IKM
from telegram import ReplyKeyboardMarkup as RKM
from telegram import ReplyKeyboardRemove as RKR
from telegram import InlineKeyboardButton as IKB
from telegram.ext import MessageHandler as MHandler
from telegram.ext import Updater, CommandHandler, Filters, CallbackQueryHandler
from Bot.filter import *
from Bot import utils, func_data
from Bot.bot_modules.constructor import construct
import logging
import configs
from datetime import datetime


# Class represents a Bot in Telegram
class LibraryBot:
    # Intialization of Bot
    # params:
    # token -- Token from BotFather
    # controller -- data base connector
    def __init__(self, token, controller):
        self.controller = controller
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.keyboard_dict = func_data.keyboard_dict
        self.types = func_data.lists["user_types"]
        self.location = {}
        self.user_data = {}

        self.dispatcher.add_handler(CommandHandler('start', self.main_menu))
        self.add_handlers()

        self.dispatcher.add_error_handler(self.error)

        self.updater.start_polling()
        self.updater.idle()

    def add_handlers(self):

        # User handlers
        self.dispatcher.add_handler(MHandler(WordFilter('Library🏤'), self.library))
        self.dispatcher.add_handler(MHandler(WordFilter('Search🔎'), self.main_menu))
        self.dispatcher.add_handler(MHandler(WordFilter('My Books📚') & UserFilter(2), self.user_orders))
        self.dispatcher.add_handler(MHandler(WordFilter('Help👤') & UserFilter(2), self.main_menu))

        f1 = (WordFilter('Books📖') | WordFilter('Journal Articles📰') | WordFilter('Audio/Video materials📼'))
        self.dispatcher.add_handler(MHandler(f1 & LocationFilter(self.location, 'library'), self.load_material))

        self.dispatcher.add_handler(MHandler(WordFilter('Registration📝') & UserFilter(0), self.registration))
        self.dispatcher.add_handler(MHandler(LocationFilter(self.location, 'reg') & Filters.text, self.reg_steps))
        self.dispatcher.add_handler(CommandHandler('get_admin', self.upto_admin, filters=UserFilter(2), pass_args=True))

        self.dispatcher.add_handler(MHandler(WordFilter('Cancel⤵️'), self.main_menu))

        # Admin handlers
        self.dispatcher.add_handler(CommandHandler('get_key', utils.get_key, filters=UserFilter(3)))
        self.dispatcher.add_handler(MHandler(WordFilter("User management 👥") & UserFilter(3), self.user_manage))

        self.dispatcher.add_handler(MHandler(WordFilter("Confirm application📝") & UserFilter(3), self.confirm))
        self.dispatcher.add_handler(MHandler(WordFilter("Check overdue📋") & UserFilter(3), self.main_menu))
        self.dispatcher.add_handler(MHandler(WordFilter("Show users👥") & UserFilter(3), self.show_users))
        self.dispatcher.add_handler(
            MHandler(LocationFilter(self.location, "user_modify") & UserFilter(3), self.modify_user))
        self.dispatcher.add_handler(
            MHandler(LocationFilter(self.location, "doc_modify") & UserFilter(3), self.update_doc_param))
        self.dispatcher.add_handler(MHandler(LocationFilter(self.location, "notice") & UserFilter(3), self.notice_user))

        self.dispatcher.add_handler(
            MHandler(WordFilter("Material management 📚") & UserFilter(3), self.mat_manage))
        self.dispatcher.add_handler(CallbackQueryHandler(self.online_button_checker))

        self.dispatcher.add_handler(MHandler(WordFilter("Add material🗄") & UserFilter(3), self.add_doc))
        self.dispatcher.add_handler(
            MHandler(f1 & UserFilter(3) & LocationFilter(self.location, 'add_doc'), self.start_adding))
        self.dispatcher.add_handler(
            MHandler(LocationFilter(self.location, 'add_doc') & Filters.text, self.adding_steps))

    # Main menu
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def main_menu(self, bot, update):
        chat = update.message.chat_id
        user_type = self.controller.user_type(chat)
        keyboard = self.keyboard_dict[self.types[user_type]]
        self.location[chat] = 'main'
        self.user_data[chat] = []
        bot.send_message(chat_id=chat, text="Main menu", reply_markup=RKM(keyboard, True))

    def check_overdue(self, bot, update):
        pass

    def get_data(self, bot, chat, location, text=None):
        n = 5
        data_list = []
        if location == 'confirm':
            data_list = self.controller.get_all_unconfirmed()
            if len(data_list) == 0:
                bot.send_message(chat_id=chat, text="There are no application to confirm")
                return
        elif location == 'library':
            doc_type = func_data.analog.get(text, text)
            data_list = self.controller.get_all_doctype(doc_type)
            if len(data_list) == 0:
                bot.send_message(chat_id=chat, text="There are no materials in the library")
                return
        elif location == "my_orders":
            data_list = self.controller.get_user_orders(chat)
            if len(data_list) == 0:
                bot.send_message(chat_id=chat, text="You do not have active orders")
                return
        elif location == 'users':
            data_list = self.controller.get_all_patrons()
            if len(data_list) == 0:
                bot.send_message(chat_id=chat, text="There are no patrons")
                return

        data_list = [data_list[i * n:(i + 1) * n] for i in range(len(data_list) // n + 1) if i * n < len(data_list)]
        max_page = len(data_list) - 1
        return data_list, max_page

    def get_message(self, loc, page, item, doc_type=None, chat=None):
        message = [0, 0]
        if loc == 'confirm':
            message[0] = """
            Check whether all data is correct:\nName: {name}\nAddress: {address}\nPhone: {phone}\nStatus: {status}
            """.format(**item)
            message[1] = IKM([[IKB("Accept✅", callback_data='accept {} {}'.format(item['id'], loc)),
                               IKB("Reject️❌", callback_data='reject {} {}'.format(item['id'], loc)),
                               IKB("Cancel⤵️", callback_data='cancel {} {}'.format(page, loc))]])
        elif loc == 'library':
            text = """Title: {title}\nAuthors: {authors}\n"""
            if doc_type == "book":
                text += """Description: {description}\nFree copy: {free_count}"""
            elif doc_type == "article":
                text += """Journal: {journal}\nIssue: {issue}\nDate: {date}\nFree copy: {free_count}"""
            elif doc_type == "media":
                text += """Free copy: {free_count}"""
            if self.controller.user_type(chat) == 2 and item['free_count'] > 0:
                keyboard = [
                    [IKB("Order the document", callback_data='order {} {} {}'.format(item['id'], doc_type, loc)),
                     IKB('Cancel', callback_data='cancel {} {} {}'.format(page, doc_type, loc))]]
            elif self.controller.user_type(chat) == 3:
                if item['free_count'] == item['count']:
                    keyboard = [[IKB('Edit', callback_data='edit {} {} {} {}'.format(page, item['id'], doc_type, loc)),
                                 IKB('Delete', callback_data='del {} {} {} {}'.format(page, item['id'], doc_type, loc)),
                                 IKB('Cancel️', callback_data='cancel {} {} {}'.format(page, doc_type, loc))]]
                else:
                    keyboard = [[IKB('Edit', callback_data='edit {} {} {} {}'.format(page, item['id'], doc_type, loc)),
                                 IKB('Cancel️', callback_data='cancel {} {} {}'.format(page, doc_type, loc))]]
            else:
                keyboard = [[IKB('Cancel️', callback_data='cancel {} {} {}'.format(page, doc_type, loc))]]
            message[0] = text.format(**item)
            message[1] = IKM(keyboard)
        if loc == 'my_orders':
            doc, time, time_out = item.values()
            message[0] = "Title: {}\nAuthors: {}\nAvailable till: {}".format(doc['title'], doc['authors'], time_out)
            message[1] = IKM([[IKB("Cancel⤵️", callback_data='cancel {} {}'.format(page, loc))]])
        if loc == 'users':
            user = item
            user_id = user['id']
            orders = self.controller.get_user_orders(user_id)
            text = """
                Name: {name}\nAddress: {address}\nPhone: {phone}\nStatus: {status}\nTaken documents: """.format(**user)
            text += "{}\nOverdue documents: ".format(len(orders))
            text += str(len([i for i in orders if datetime.strptime(i['time_out'], "%Y-%m-%d") < datetime.today()]))
            keyboard = [[IKB("Edit", callback_data='edit {} {} {}'.format(page, user_id, loc)),
                         IKB('Cancel️', callback_data='cancel {} {} {}'.format(page, doc_type, loc))]]
            if orders:
                keyboard[0].insert(1, IKB("Orders", callback_data='orders {} {} {}'.format(page, user_id, loc)))
            else:
                keyboard[0].insert(1, IKB("Delete", callback_data='delete {} {} {}'.format(page, user_id, loc)))
            message[0] = text.format(**user)
            message[1] = IKM(keyboard)

        return message

    def online_init(self, bot, update):
        chat = update.message.chat_id
        loc = self.location[chat]
        text = update.message.text
        data_list, max_page = self.get_data(bot, chat, loc, text)
        if not data_list:
            return
        text_message = func_data.text_gen(data_list, loc)
        if loc == 'library':
            loc = func_data.analog[text] + " " + loc

        keyboard = [
            [IKB(str(i + 1), callback_data="item {} {} {}".format(i, 0, loc)) for i in range(len(data_list[0]))]]
        keyboard += [[IKB("⬅", callback_data='prev 0 {} ' + loc), IKB("➡️", callback_data='next 0 ' + loc)]]
        update.message.reply_text(text=text_message + "\n\nCurrent page: 1/" + str(max_page + 1),
                                  reply_markup=IKM(keyboard))

    def online_button_checker(self, bot, update):
        query = update.callback_query
        chat = query.message.chat.id
        message_id = query.message.message_id
        action, *args, loc = query.data.split(" ")
        data_list, max_page = self.get_data(bot, chat, loc, args[-1])
        if not data_list:
            return

        if action in ['prev', 'next'] and max_page or action == 'cancel':
            page = int(args[0])
            if action == "next":
                page = 0 if page == max_page else page + 1
            if action == "prev":
                page = max_page if page == 0 else page - 1
            text_message = func_data.text_gen(data_list, loc, page)
            if loc == 'library':
                loc = args[-1] + " " + loc
            keyboard = [[IKB(str(i + 1), callback_data="item {} {} {}".format(i, page, loc)) for i in
                         range(len(data_list[page]))]]
            keyboard += [[IKB("⬅", callback_data='prev {} {}'.format(page, loc)),
                          IKB("➡️", callback_data='next {} {}'.format(page, loc))]]
            bot.edit_message_text(text=text_message + "\n\nCurrent page: {}/{}".format(page + 1, max_page + 1),
                                  chat_id=chat,
                                  message_id=message_id, reply_markup=IKM(keyboard))
        elif action == 'item':
            k = int(args[0])
            page = int(args[1])
            item = data_list[page][k]
            message = self.get_message(loc, page, item, args[-1], chat)
            bot.edit_message_text(chat_id=chat, message_id=message_id, text=message[0], reply_markup=message[1])
        elif action in ['accept', 'reject'] and loc == 'confirm':
            user_id = int(args[0])
            ids = [chat, message_id]
            self.conf_user(bot, ids, user_id, action)
        elif loc == 'library':
            ids = [chat, message_id]
            self.modify_document(bot, ids, action, args)
        elif loc == 'users':
            ids = [chat, message_id]
            self.user_flip(bot, ids, action, args)

    def error(self, bot, update, error):
        """Log Errors caused by Updates."""
        self.logger.warning('Update "%s" caused error "%s"', update, error)


# Start Bot
# params:
#  Controller -- Bot's data base
def start_bot(controller):
    construct(LibraryBot)
    LibraryBot(configs.token, controller)
