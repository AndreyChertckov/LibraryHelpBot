import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardRemove, \
    InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from Bot.filter import *
from Bot.books import books, users
import logging
from

token = '315702006:AAFwvs4RhsVmTCVPTvknedvxPSs7t_8KfJE'


class LibraryBot:
    def __init__(self, token):
        self.bot = telegram.Bot(token=token)
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.keyboard_dict = {
            "unauth": [['Registration📝', 'Library🏤', 'Search🔎', 'Help👤']],
            "auth": [['Library🏤', 'Search🔎', 'My Books📚', 'Help👤']],
            "admin": [['5', '6', '7', '8']],
            "reg_confirm": [["All is correct✅", "Something is incorrect❌"]],
            "lib_main": [['Books📖', 'Journal Articles📰', "Audio/Video materials📼", "Cancel"]]
        }

        start_handler = CommandHandler('start', self.start)
        reg_handler = MessageHandler(UserFilter("u") & WordFilter('Registration📝'), self.registration)

        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(reg_handler)
        self.updater.start_polling()
        print(self.dispatcher.handlers)
        self.updater.idle()

    def start(self, bot, update):
        print(update.message.chat_id, list(users.keys()), update.message.from_user)
        if update.message.chat_id in list(users.keys()):
            if users[update.message.chat_id][0]:
                keyboard = self.keyboard_dict["auth"]
            else:
                keyboard = self.keyboard_dict["admin"]
        else:
            keyboard = self.keyboard_dict["unauth"]

        bot.send_message(chat_id=update.message.chat_id, text="I'm bot, Hello",
                         reply_markup=telegram.ReplyKeyboardMarkup(keyboard, True))

    def registration(self, bot, update):
        self.new_user = {"id": update.message.chat_id}
        self.field = ["name", "address", "phone number", "status"]
        self.reg_step = 0
        self.is_in_reg = True
        text_for_message = """
            During registration you have to provide your name, address, phone number and status (student or faculty).\n
            Example:
            Ivan Ivanov,
            ul. Universitetskaya 1, 2-100,
            +71234567890,
            Student     
        """
        bot.send_message(chat_id=update.message.chat_id, text=text_for_message)
        self.reg_step_handler = MessageHandler(BooleanFilter(self.is_in_reg) & Filters.text, self.reg_steps)
        self.dispatcher.add_handler(self.reg_step_handler)
        bot.send_message(chat_id=update.message.chat_id, text="Enter your name", reply_markup=ReplyKeyboardRemove([[]]))

    def reg_steps(self, bot, update):
        if self.reg_step < len(self.field):
            self.new_user[self.field[self.reg_step]] = update.message.text
            self.reg_step += 1
            if self.reg_step < len(self.field):
                bot.send_message(chat_id=update.message.chat_id, text="Enter your {}".format(self.field[self.reg_step]),
                                 reply_markup=self.low_menu)
            else:
                text_for_message = """
                    Check whether all data is correct:
                    Name: {}
                    Adress: {}
                    Phone: {}
                    Status: {}
                """.format(*list(self.new_user.values())[1:])
                bot.send_message(chat_id=update.message.chat_id, text=text_for_message,
                                 reply_markup=ReplyKeyboardMarkup(self.keyboard_dict["reg_confirm"]))
        elif self.reg_step == len(self.field):
            if update.message.text == "All is correct✅":
                self.is_in_reg = False
                users[self.new_user['id']] = {i: self.new_user[i] for i in self.field}
                del self.reg_step
                del self.field
                del self.new_user
                open("file.txt", "a").write(str(users))
                bot.send_message(chat_id=update.message.chat_id, text="You have been registered",
                                 reply_markup=telegram.ReplyKeyboardMarkup(self.keyboard_dict["auth"], True))
                self.dispatcher.handlers[0].remove(self.reg_step_handler)
            elif update.message.text == "Something is incorrect❌":
                self.new_user = {"id": update.message.chat_id}
                self.reg_step = 0
                bot.send_message(chat_id=update.message.chat_id, text="Enter your name",
                                 reply_markup=ReplyKeyboardRemove([[]]))

    def cho_to(self):


    def lib_handler(self):
        library_handler = MessageHandler(WordFilter('Library🏤'), self.library)

        self.in_lib = False  # In library or not
        self.numpage = 0 # Number of page
        #test list (pagess)
        self.pagess = list([["books" + str(j) + " " + str(i)] for i in range(10)] for j in range(10))
        #Hadlrers for library
        # self.dispatcher.add_handler(
        #     MessageHandler(BooleanFilter(self.in_lib) & WordFilter('<-'), self.library))
        # self.dispatcher.add_handler(
        #     MessageHandler(WordFilter('->'), self.library))
        # self.dispatcher.add_handler(
        #     MessageHandler(BooleanFilter(self.in_lib) & WordFilter('cancel'), self.cancel))
        #
        # self.dispatcher.add_handler(library_handler)
        #End handlers for library


    # def caps(self, bot, update):
    #     # text_caps = ' '.join(args).upper()
    #     # bot.send_message(chat_id=update.message.chat_id, text=text_caps)
    #     button_list = [
    #         InlineKeyboardButton("col1", url="https://vk.com/feed"),
    #         InlineKeyboardButton("col2", callback_data="2"),
    #         InlineKeyboardButton("row 2", callback_data="3")
    #     ]
    #     reply_markup = InlineKeyboardMarkup(self.build_menu(button_list, n_cols=2))
    #     bot.send_message(chat_id=update.message.chat_id, text="Blb", reply_markup=reply_markup)
    #
    # def build_menu(self, buttons, n_cols, header_buttons=None, footer_buttons=None):
    #     menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    #     if header_buttons:
    #         menu.insert(0, header_buttons)
    #     if footer_buttons:
    #         menu.append(footer_buttons)
    #     return menu


#Search in library
#!!!!Надо доделать cancel и дальнейший сценарий
    # def library(self, bot, update):
    #     print(self.numpage)
    #     print(len(self.pagess))
    #     self.in_lib = True
    #     if update.message.text == '<-':
    #         self.numpage -= 1
    #     elif update.message.text == '->':
    #         self.numpage += 1
    #     else:
    #         self.numpage = 0
    #     if self.numpage < 0 and self.numpage+1 >= len(self.pagess) :
    #         return
    #     # print(pages)
    #     keyboard = self.pagess[self.numpage] + [["<-", "->"], ["Cancel"]]
    #     reply_markup = ReplyKeyboardMarkup(keyboard)
    #     print("=======")
    #     bot.send_message(chat_id=update.message.chat_id, text="My set of books!", reply_markup=reply_markup)
    # def cancel(self,bot,update):
    #     pass

LibraryBot(token)
