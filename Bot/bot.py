import telegram
from telegram import InlineKeyboardMarkup as IKM
from telegram import ReplyKeyboardMarkup as RKM
from telegram import ReplyKeyboardRemove as RKR
from telegram import InlineKeyboardButton as IKB
from telegram.ext import MessageHandler as MessageH, Updater, CommandHandler, Filters, CallbackQueryHandler
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
        # self.updater = Updater(token=token)
        self.updater = Updater(token=token, request_kwargs={
            'proxy_url': 'socks5://196.18.15.159:8000',
            'urllib3_proxy_kwargs': {'username': 'Q5aawZ', 'password': 'dN0xJX'}})
        self.dispatcher = self.updater.dispatcher
        self.bot = self.updater.bot
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.keyboard_dict = func_data.keyboard_dict
        self.types = func_data.lists['user_types']
        self.location = {}
        self.user_data = {}
        self.add_handlers()

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

    def add_handlers(self):
        self.dispatcher.add_handler(CommandHandler('start', self.main_menu))
        # User handlers
        self.dispatcher.add_handler(CallbackQueryHandler(self.online_button_checker))

        self.dispatcher.add_handler(MessageH(WordFilter('Library🏤'), self.library))
        self.dispatcher.add_handler(MessageH(WordFilter('Search🔎'), self.start_search))
        self.dispatcher.add_handler(MessageH(WordFilter('My Books📚') & UserFilter(2), self.user_orders))
        self.dispatcher.add_handler(MessageH(WordFilter('Help👤') & UserFilter(2), self.main_menu))

        f1 = (WordFilter('Books📖') | WordFilter('Journal Articles📰') | WordFilter('Audio/Video materials📼'))
        self.dispatcher.add_handler(MessageH(f1 & LocFilter(self.location, 'library'), self.load_material))
        self.dispatcher.add_handler(MessageH(f1 & LocFilter(self.location, 'search'), self.enter_search))
        self.dispatcher.add_handler(MessageH(LocFilter(self.location, 'search') & Filters.text, self.search))

        self.dispatcher.add_handler(MessageH(WordFilter('Registration📝') & UserFilter(0), self.registration))
        self.dispatcher.add_handler(MessageH(LocFilter(self.location, 'reg') & Filters.text, self.reg_steps))
        self.dispatcher.add_handler(CommandHandler('get_admin', self.verification, pass_args=True))

        self.dispatcher.add_handler(MessageH(WordFilter('Cancel⤵️'), self.main_menu))

        # Admin handlers
        self.dispatcher.add_handler(CommandHandler('get_key', utils.get_key, filters=UserFilter(3)))
        self.dispatcher.add_handler(MessageH(WordFilter('User management 👥') & UserFilter(3), self.user_manage))

        self.dispatcher.add_handler(MessageH(WordFilter('Confirm application📝') & UserFilter(3), self.confirm))
        self.dispatcher.add_handler(MessageH(WordFilter('Check overdue📋') & UserFilter(3), self.main_menu))
        self.dispatcher.add_handler(MessageH(WordFilter('Show users👥') & UserFilter(3), self.show_users))
        self.dispatcher.add_handler(MessageH(LocFilter(self.location, 'user_modify') & UserFilter(3), self.modify_user))
        self.dispatcher.add_handler(MessageH(LocFilter(self.location, 'doc_modify') & UserFilter(3), self.update_doc_param))
        self.dispatcher.add_handler(MessageH(LocFilter(self.location, 'notice') & UserFilter(3), self.notice_user))

        self.dispatcher.add_handler(MessageH(WordFilter('Material management 📚') & UserFilter(3), self.mat_manage))

        self.dispatcher.add_handler(MessageH(WordFilter('Add material🗄') & UserFilter(3), self.add_doc))
        self.dispatcher.add_handler(MessageH(f1 & UserFilter(3) & LocFilter(self.location, 'add_doc'), self.start_adding))
        self.dispatcher.add_handler(MessageH(LocFilter(self.location, 'add_doc') & Filters.text, self.adding_steps))

        self.dispatcher.add_error_handler(self.error)

    # Main menu
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def main_menu(self, bot, update):
        chat_id = update.message.chat_id
        user_type = self.controller.user_type(chat_id)
        keyboard = self.keyboard_dict[self.types[user_type]]
        self.location[chat_id] = 'main'
        self.user_data[chat_id] = []
        bot.send_message(chat_id=chat_id, text='Main menu', reply_markup=RKM(keyboard, True))

    def check_overdue(self, bot, update):
        pass

    def get_data(self, bot, chat_id, location, *text):
        n = 5
        data_list = []
        if location == 'confirm':
            data_list = self.controller.get_all_unconfirmed()
        elif location == 'library':
            doc_type = func_data.analog.get(text[0], text[0])
            data_list = self.controller.get_all_doctype(doc_type)
        elif location == 'my_orders':
            data_list = self.controller.get_user_orders(chat_id)
        elif location == 'users':
            data_list = self.controller.get_all_patrons()
        elif location == 'search':
            doc_type = func_data.analog.get(text[0], text[0])
            data_list = self.controller.get_all_doctype(doc_type)
            sep = lambda x: x['title'].lower().find(text[1]) >= 0 or \
                            x['authors'].lower().find(text[1]) >= 0 or \
                            x['keywords'].lower().find(text[1]) >= 0
            data_list = list(filter(sep, data_list))

        if len(data_list) == 0:
            bot.send_message(chat_id=chat_id, text=func_data.empty_list[location])
            return [], 0

        data_list = [data_list[i: i + n] for i in range(0, len(data_list), n)]
        max_page = len(data_list) - 1
        return data_list, max_page

    def get_message(self, loc, page, item, doc_type=None, chat_id=None, add_text=''):
        message = [0, 0]
        if loc == 'confirm':
            message[0] = 'Check whether all data is correct:\nName: {name}' \
                         '\nAddress: {address}\nPhone: {phone}\nStatus: {status}'.format(**item)
            message[1] = IKM([[IKB('Accept✅', callback_data='accept {} {}'.format(item['id'], loc)),
                               IKB('Reject️❌', callback_data='reject {} {}'.format(item['id'], loc)),
                               IKB('Cancel⤵️', callback_data='cancel {} {}'.format(page, loc))]])
        elif loc in ['library', 'search']:
            text = 'Title: {title}\nAuthors: {authors}\n'
            if doc_type == 'book':
                text += 'Description: {description}\nFree copy: {free_count}'
            elif doc_type == 'article':
                text += 'Journal: {journal}\nIssue: {issue}\nDate: {date}\nFree copy: {free_count}'
            elif doc_type == 'media':
                text += 'Free copy: {free_count}'
            doc_type = add_text + " " + doc_type if add_text else doc_type
            if self.controller.user_type(chat_id) == 2:
                cb = 'order {} {} {}' if item['free_count'] > 0 else 'queue {} {} {}'
                keyboard = [[IKB('Order the document', callback_data=cb.format(item['id'], doc_type, loc)),
                             IKB('Cancel', callback_data='cancel {} {} {}'.format(page, doc_type, loc))]]
            elif self.controller.user_type(chat_id) == 3:
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
            keys = ['user_id', 'doc', 'table', 'time', 'time_out', 'active', 'id']
            user, doc, doc_type, time, time_out, active, order_id = [item[i] for i in keys]
            message[0] = 'Title: {}\nAuthors: {}\nAvailable till: {}'.format(doc['title'], doc['authors'], time_out)
            keyboard = []
            if active and not [j for i in utils.to_list(doc['queue']) for j in i]:
                keyboard += [IKB('Renew🔄', callback_data='renew {} {}'.format(order_id, loc))]
            elif not active:
                keyboard += [IKB('Repeal❌', callback_data='repeal {} {}'.format(order_id, loc))]
            keyboard += [IKB('Cancel⤵️', callback_data='cancel {} {}'.format(page, loc))]
            message[1] = IKM([keyboard])
        if loc == 'users':
            user = item
            user_id = user['id']
            orders = self.controller.get_user_orders(user_id)
            text = 'Name: {name}\nAddress: {address}\nPhone: {phone}\nStatus: {status}\nTaken documents: '.format(
                **user)
            text += '{}\nOverdue documents: '.format(len(orders))
            overdue = filter(lambda i: datetime.strptime(i['time_out'], '%Y-%m-%d') < datetime.today(), orders)
            text += str(len(list(overdue)))
            keyboard = [[IKB('Edit', callback_data='edit {} {} {}'.format(page, user_id, loc)),
                         IKB('Cancel️', callback_data='cancel {} {} {}'.format(page, doc_type, loc))]]
            if orders:
                keyboard[0].insert(1, IKB('Orders', callback_data='orders {} {} {}'.format(page, user_id, loc)))
            else:
                keyboard[0].insert(1, IKB('Delete', callback_data='delete {} {} {}'.format(page, user_id, loc)))
            message[0] = text.format(**user)
            message[1] = IKM(keyboard)

        return message

    def online_init(self, bot, update):
        chat_id = update.message.chat_id
        loc = self.location[chat_id]
        text = update.message.text
        add_data, text = (text, self.user_data[chat_id][0]) if loc == 'search' else ('', text)
        data_list, max_page = self.get_data(bot, chat_id, loc, text, add_data)
        if not data_list:
            return
        text_message = func_data.text_gen(data_list, loc, add_text=text)
        if loc == 'library':
            loc = func_data.analog[text] + ' ' + loc
        if loc == 'search':
            loc = '{} {} {}'.format(self.user_data[chat_id][0], text, loc)

        keyboard = [[IKB(str(i + 1), callback_data='item {} {} {}'.format(i, 0, loc)) for i in range(len(data_list[0]))]]
        keyboard += [[IKB('⬅', callback_data='prev 0 {} ' + loc), IKB('➡️', callback_data='next 0 ' + loc)]]
        update.message.reply_text(text=text_message + '\n\nCurrent page: 1/' + str(max_page + 1),
                                  reply_markup=IKM(keyboard))

    def online_button_checker(self, bot, update):
        query = update.callback_query
        chat_id = query.message.chat.id
        message_id = query.message.message_id
        action, *args, loc = query.data.split(' ')
        add_data = args[-2] if loc == 'search' else ''
        data_list, max_page = self.get_data(bot, chat_id, loc, args[-1], add_data)
        if not data_list:
            return

        if action in ['prev', 'next'] and max_page or action == 'cancel':
            page = int(args[0])
            if action == 'next':
                page = 0 if page == max_page else page + 1
            if action == 'prev':
                page = max_page if page == 0 else page - 1
            text_message = func_data.text_gen(data_list, loc, page)
            if loc == 'library':
                loc = args[-1] + ' ' + loc
            if loc == 'search':
                loc = '{} {} {}'.format(*args[-2:], loc)
            keyboard = [[IKB(str(i + 1), callback_data='item {} {} {}'.format(i, page, loc)) for i in
                         range(len(data_list[page]))]]
            keyboard += [[IKB('⬅', callback_data='prev {} {}'.format(page, loc)),
                          IKB('➡️', callback_data='next {} {}'.format(page, loc))]]
            bot.edit_message_text(text=text_message + '\n\nCurrent page: {}/{}'.format(page + 1, max_page + 1),
                                  chat_id=chat_id, message_id=message_id, reply_markup=IKM(keyboard))
        elif action == 'item':
            k = int(args[0])
            page = int(args[1])
            item = data_list[page][k]
            message = self.get_message(loc, page, item, args[-1], chat_id, add_data)
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message[0], reply_markup=message[1])
        elif action in ['accept', 'reject'] and loc == 'confirm':
            user_id = int(args[0])
            ids = [chat_id, message_id]
            self.conf_user(bot, ids, user_id, action)
        elif loc == 'library':
            ids = [chat_id, message_id]
            self.modify_document(bot, ids, action, args)
        elif loc == 'users':
            ids = [chat_id, message_id]
            self.user_flip(bot, ids, action, args)
        elif loc == 'my_orders':
            ids = [chat_id, message_id]
            self.manage_orders(bot, ids, action, args)


    def get_bot(self):
        return self.bot

    def error(self, bot, update, error):
        """Log Errors caused by Updates."""
        self.logger.warning('Update "%s" caused error "%s"', update, error)


# Start Bot
# params:
#  Controller -- Bot's data base
def start_bot(controller):
    construct(LibraryBot)
    return LibraryBot(configs.token, controller)
