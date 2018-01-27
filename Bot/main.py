import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardRemove, \
    InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from filter import *
from books import books, users
import logging

token = '537025892:AAHqwqWaGEKdb4bBBQ9CJlKGa8mAqz7fElI'


class LibraryBot:
    def __init__(self, token):
        self.bot = telegram.Bot(token=token)
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.in_lib = False  # In library or not
        self.numpage = 0 # Number of page
        #test list (pagess)
        self.pagess = list([["books" + str(j) + " " + str(i)] for i in range(10)] for j in range(10))
        start_handler = CommandHandler('start', self.start)
        reg_handler = MessageHandler(UserFilter("u") & WordFilter('Registration'), self.registration)
        library_handler = MessageHandler(WordFilter('library'), self.library)
        #Hadlrers for library
        self.dispatcher.add_handler(
            MessageHandler(BooleanFilter(self.in_lib) & WordFilter('<-'), self.library))
        self.dispatcher.add_handler(
            MessageHandler( WordFilter('->'), self.library))
        self.dispatcher.add_handler(
            MessageHandler(BooleanFilter(self.in_lib) & WordFilter('cancel'), self.cancel))
        self.dispatcher.add_handler(library_handler)
        #End handlers for library
        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(reg_handler)
        self.updater.start_polling()
        # self.dispatcher.handlers[0].remove(start_handler)
        # print(self.dispatcher.handlers[0])
        self.updater.idle()

    def start(self, bot, update):
        print(update.message.chat_id, list(users.keys()), update.message.from_user)
        if update.message.chat_id in list(users.keys()):
            if users[update.message.chat_id][0]:
                self.keyboard = [['1', '2', '3', '4']]
            else:
                self.keyboard = [['5', '6', '7', '8']]
        else:
            self.keyboard = [['Registration', '9', '0']]

        self.low_menu = telegram.ReplyKeyboardMarkup(self.keyboard, True)
        bot.send_message(chat_id=update.message.chat_id, text="I'm bot, Hello",
                         reply_markup=self.low_menu)

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
        rkeyboard = [[]]
        self.low_menu = ReplyKeyboardRemove(rkeyboard)
        bot.send_message(chat_id=update.message.chat_id, text="Enter your name", reply_markup=self.low_menu)

    def reg_steps(self, bot, update):
        if self.reg_step < len(self.field):
            self.new_user[self.field[self.reg_step]] = update.message.text
            self.reg_step += 1
            if self.reg_step < len(self.field):
                bot.send_message(chat_id=update.message.chat_id, text="Enter your {}".format(self.field[self.reg_step]),
                                 reply_markup=self.low_menu)
            else:
                print(list(self.new_user.values())[1:])
                text_for_message = """
                    Check whether all data is correct:
                    Name: {}
                    Adress: {}
                    Phone: {}
                    Status: {}
                """.format(*list(self.new_user.values())[1:])
                rkeyboard = [["All is correct", "Something is incorrect"]]
                self.low_menu = ReplyKeyboardMarkup(rkeyboard)
                bot.send_message(chat_id=update.message.chat_id, text=text_for_message, reply_markup=self.low_menu)
        elif self.reg_step == len(self.field):
            if update.message.text == "All is correct":
                self.is_in_reg = False
                del self.reg_step
                users[self.new_user['id']] = {i: self.new_user[i] for i in self.field}
                del self.field
                del self.new_user
                open("file.txt", "a").write(str(users))
                self.keyboard = [['1', '2', '3', '4']]
                self.low_menu = telegram.ReplyKeyboardMarkup(self.keyboard, True)
                bot.send_message(chat_id=update.message.chat_id, text="You have been registered",
                                 reply_markup=self.low_menu)
            elif update.message.text == "Something is incorrect":
                self.new_user = {"id": update.message.chat_id}
                self.reg_step = 0
                rkeyboard = [[]]
                self.low_menu = ReplyKeyboardRemove(rkeyboard)
                bot.send_message(chat_id=update.message.chat_id, text="Enter your name", reply_markup=self.low_menu)

    def caps(self, bot, update):
        # text_caps = ' '.join(args).upper()
        # bot.send_message(chat_id=update.message.chat_id, text=text_caps)
        button_list = [
            InlineKeyboardButton("col1", url="https://vk.com/feed"),
            InlineKeyboardButton("col2", callback_data="2"),
            InlineKeyboardButton("row 2", callback_data="3")
        ]
        reply_markup = InlineKeyboardMarkup(self.build_menu(button_list, n_cols=2))
        bot.send_message(chat_id=update.message.chat_id, text="Blb", reply_markup=reply_markup)

    def build_menu(self, buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu
#Search in library
#!!!!Надо доделать cancel и дальнейший сценарий
    def library(self, bot, update):
        print(self.numpage)
        print(len(self.pagess))
        self.in_lib = True
        if update.message.text == '<-':
            self.numpage -= 1
        elif update.message.text == '->':
            self.numpage += 1
        else:
            self.numpage = 0
        if self.numpage < 0 and self.numpage+1 >= len(self.pagess) :
            return
        # print(pages)
        keyboard = self.pagess[self.numpage] + [["<-", "->"], ["Cancel"]]
        reply_markup = ReplyKeyboardMarkup(keyboard)
        print("=======")
        bot.send_message(chat_id=update.message.chat_id, text="My set of books!", reply_markup=reply_markup)
    def cancel(self,bot,update):
        pass

LibraryBot(token)
