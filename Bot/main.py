import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardRemove, \
    InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from Bot.filter import *
from Bot import utils
import logging
import configs


class LibraryBot:
    def __init__(self, token, cntrl):
        self.cntrl = cntrl
        self.bot = telegram.Bot(token=token)
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.keyboard_dict = {
            "unauth": [['Registration📝', 'Library🏤', 'Search🔎', 'Help👤']],
            "auth": [['Library🏤', 'Search🔎', 'My Books📚', 'Help👤']],
            "admin": [["Check material", "Material management", "User management"]],
            "mat_manage": [[]],
            "user_manage": [[]],
            "reg_confirm": [["All is correct✅", "Something is incorrect❌"]],
            "lib_main": [['Books📖', 'Journal Articles📰', "Audio/Video materials📼", "Cancel⤵️"]],
            "cancel": [['Cancel⤵']],
            "status": [['Student', 'Faculty (professor, instructor, TA)']]
        }
        self.is_in_reg = {}

        start_handler = CommandHandler('start', self.start)
        reg_handler = MessageHandler(UserFilter("unreg") & WordFilter('Registration📝'), self.registration)
        reg_admin_handler = CommandHandler('get_admin', self.reg_admin, filters=UserFilter("patron"), pass_args=True)
        get_key_handler = CommandHandler('get_key', utils.get_key, filters=UserFilter("libr"))
        library_handler = MessageHandler(WordFilter('Library🏤'), self.library)
        cancel_handler = MessageHandler(WordFilter('Cancel⤵️'), self.cancel)

        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(reg_handler)
        self.dispatcher.add_handler(reg_admin_handler)
        self.dispatcher.add_handler(get_key_handler)
        self.dispatcher.add_handler(library_handler)
        self.dispatcher.add_handler(cancel_handler)

        self.updater.start_polling()
        self.updater.idle()

    def start(self, bot, update):
        if self.cntrl.chat_exists(update.message.chat_id):
            if self.cntrl.get_user(update.message.chat_id)['status'] == 'librarian':
                keyboard = self.keyboard_dict["admin"]
            else:
                keyboard = self.keyboard_dict["auth"]
        else:
            keyboard = self.keyboard_dict["unauth"]

        self.keyboardmarkup = telegram.ReplyKeyboardMarkup(keyboard, True)
        bot.send_message(chat_id=update.message.chat_id, text="I'm bot, Hello",
                         reply_markup=self.keyboardmarkup)

    def reg_admin(self, bot, update, args):
        if args[0] == open('Bot/key.txt').read():
            self.cntrl.upto_librarian(update.message.chat_id)
            self.keyboardmarkup = telegram.ReplyKeyboardMarkup(self.keyboard_dict["admin"], True)
            bot.send_message(chat_id=update.message.chat_id, text="You have been update to Librarian",
                             reply_markup=self.keyboardmarkup)
            utils.key_gen()

    def registration(self, bot, update):
        self.new_user = {"id": update.message.chat_id}          # заготовка под нового юзера
        self.field = ["name", "address", "phone", "status"]     # шаги регистрации
        self.reg_step = 0                                       # текущий шаг регистрации
        self.is_in_reg = [update.message.chat_id, True]
        text_for_message = """
            During registration you have to provide your name, address, phone number and status (student or faculty).\n
            Example:
            Ivan Ivanov,
            ul. Universitetskaya 1, 2-100,
            +71234567890,
            Student     
        """
        bot.send_message(chat_id=update.message.chat_id, text=text_for_message)
        self.reg_step_handler = MessageHandler(UserFilter(self.is_in_reg) & Filters.text, self.reg_steps)
        self.dispatcher.add_handler(self.reg_step_handler)      # хандлер для фиксирования сообщений при регистраци
        self.keyboardmarkup.keyboard = [[]]
        bot.send_message(chat_id=update.message.chat_id, text="Enter your name", reply_markup=ReplyKeyboardRemove([[]]))

    def reg_steps(self, bot, update):
        if self.reg_step < len(self.field):  # Если шаг регистрации не последний
            text = update.message.text
            self.new_user[self.field[self.reg_step]] = text if text != "Faculty (professor, instructor, TA)" else "Faculty"
            self.reg_step += 1
            if self.reg_step < len(self.field):     # Если после итерации на предыдущей линии этап всё ещё не последний
                                                    # просим следующие данные
                if self.field[self.reg_step] == "status":
                    self.keyboardmarkup = telegram.ReplyKeyboardMarkup(self.keyboard_dict["status"], True)
                bot.send_message(chat_id=update.message.chat_id, text="Enter your {}".format(self.field[self.reg_step]),
                                 reply_markup=self.keyboardmarkup)

            else:  # иначе просим подтверждения корректнсти данных
                text_for_message = """
                    Check whether all data is correct:
                    Name: {name}
                    Adress: {address}
                    Phone: {phone}
                    Status: {status}
                """.format(**self.new_user)
                bot.send_message(chat_id=update.message.chat_id, text=text_for_message,
                                 reply_markup=ReplyKeyboardMarkup(self.keyboard_dict["reg_confirm"], True))
        elif self.reg_step == len(self.field):  # Если это последний шаг регистрации
            if update.message.text == "All is correct✅":  # Если всё верно
                self.is_in_reg = False
                del self.reg_step
                del self.field
                self.cntrl.registration(self.new_user)   # Добавляем пользователя в бд
                self.keyboardmarkup = telegram.ReplyKeyboardMarkup(self.keyboard_dict["auth"], True)

                del self.new_user  # Возвращаем пользователю
                bot.send_message(chat_id=update.message.chat_id, text="Your request has been sent.\n Wait for librarian confirmation",     # интерфейс зарегистрированного
                                 reply_markup=self.keyboardmarkup)
                self.dispatcher.handlers[0].remove(self.reg_step_handler)
            elif update.message.text == "Something is incorrect❌":  # Если что-то неверно, то возвращаем
                self.new_user = {"id": update.message.chat_id}       # параметры в начальное состояние
                self.reg_step = 0
                self.keyboardmarkup.keyboard = [[]]
                bot.send_message(chat_id=update.message.chat_id, text="Enter your name",
                                 reply_markup=ReplyKeyboardRemove([[]]))

    # def lib_handler(self):
    #     library_handler = MessageHandler(WordFilter('Library🏤'), self.library)
    #     self.dispatcher.add_handler(
    #             MessageHandler(BooleanFilter(self.keyboardmarkup.keyboard==self.keyboard_dict[lib]) & WordFilter('<-'), self.library))
    #
    #     self.dispatcher.add_handler(library_handler)


    def library(self, bot, update):
        self.keyboardmarkup = telegram.ReplyKeyboardMarkup(self.keyboard_dict["lib_main"], True)
        book_handler = MessageHandler(WordFilter('Books📖') & LocationFilter(self, "lib_main"), self.cancel)
        article_handler = MessageHandler(WordFilter('Journal Articles📰️') & LocationFilter(self, "lib_main"),
                                         self.cancel)
        av_handler = MessageHandler(WordFilter('Audio/Video materials📼') & LocationFilter(self, "lib_main"),
                                    self.cancel)

        self.dispatcher.add_handler(book_handler)
        self.dispatcher.add_handler(article_handler)
        self.dispatcher.add_handler(av_handler)

        bot.send_message(chat_id=update.message.chat_id, text="Choose type of material",
                         reply_markup=self.keyboardmarkup)

    def load_material(self, bot, update):
        pass

    def cancel(self, bot, update):
        user_id = update.message.chat_id
        if not self.cntrl.chat_exists(user_id):
            self.keyboardmarkup = telegram.ReplyKeyboardMarkup(self.keyboard_dict["unauth"], True)
        elif self.cntrl.get_user(user_id)['status'] != "librarian":
            self.keyboardmarkup = telegram.ReplyKeyboardMarkup(self.keyboard_dict["auth"], True)
        else:
            self.keyboardmarkup = telegram.ReplyKeyboardMarkup(self.keyboard_dict["admin"], True)

        bot.send_message(chat_id=update.message.chat_id, text="Main menu", reply_markup=self.keyboardmarkup)


        # self.pagess = list([["books" + str(j) + " " + str(i)] for i in range(10)] for j in range(10))
        # Hadlrers for library

        # self.dispatcher.add_handler(
        #     MessageHandler(WordFilter('->'), self.library))
        # self.dispatcher.add_handler(
        #     MessageHandler(BooleanFilter(self.in_lib) & WordFilter('cancel'), self.cancel))
        #
        #
        # End handlers for library


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

        # Search in library
        # !!!!Надо доделать cancel и дальнейший сценарий
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


def start_bot(controller):
    LibraryBot(configs.token, controller)
