import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, \
    InlineKeyboardButton, KeyboardButton, CallbackQuery
from telegram import ReplyKeyboardMarkup as KeyboardM
from telegram import ReplyKeyboardRemove as KeyboardR
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from Bot.filter import *
from Bot import utils
import logging
import configs


# Class represents a Bot in Telegram
class LibraryBot:
    # Intialization of Bot
    # params:
    # token -- Token from BotFather
    # cntrl -- Bot's data base
    def __init__(self, token, cntrl):
        self.cntrl = cntrl
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.keyboard_dict = {
            "unauth": [['Registration📝', 'Library🏤', 'Search🔎', 'Help👤']],
            "unconf": [['Library🏤', 'Search🔎', 'Help👤']],
            "auth": [['Library🏤', 'Search🔎', 'My Books📚', 'Help👤']],
            "admin": [["Check material", "Material management", "User management"]],
            "mat_manage": [[]],
            "user_manage": [["Confirm application", "Check overdue", "Show users"]],
            "reg_confirm": [["All is correct✅", "Something is incorrect❌"]],
            "lib_main": [['Books📖', 'Journal Articles📰', "Audio/Video materials📼", "Cancel⤵️"]],
            "cancel": [['Cancel⤵']],
            "status": [['Student', 'Faculty (professor, instructor, TA)']]
        }
        self.is_in_reg = {}

        start_handler = CommandHandler('start', self.start)
        reg_handler = MessageHandler(UserFilter("unreg") & WordFilter('Registration📝'), self.registration)
        reg_step_handler = MessageHandler(RegFilter(self.is_in_reg) & Filters.text, self.reg_steps)
        reg_admin_handler = CommandHandler('get_admin', self.reg_admin, filters=UserFilter("patron"), pass_args=True)
        get_key_handler = CommandHandler('get_key', utils.get_key, filters=UserFilter("libr"))
        library_handler = MessageHandler(WordFilter('Library🏤'), self.library)
        cancel_handler = MessageHandler(WordFilter('Cancel⤵️'), self.cancel)

        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(reg_handler)
        self.dispatcher.add_handler(reg_step_handler)
        self.dispatcher.add_handler(reg_admin_handler)
        self.dispatcher.add_handler(get_key_handler)
        self.dispatcher.add_handler(library_handler)
        self.dispatcher.add_handler(cancel_handler)

        self.updater.start_polling()
        self.updater.idle()

    # Main menu
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def start(self, bot, update):
        if self.cntrl.chat_exists(update.message.chat_id):
            if self.cntrl.get_user(update.message.chat_id)['status'] == 'librarian':
                keyboard = self.keyboard_dict["admin"]
            else:
                keyboard = self.keyboard_dict["auth"]
        else:
            keyboard = self.keyboard_dict["unauth"]

        bot.send_message(chat_id=update.message.chat_id, text="I'm bot, Hello",
                         reply_markup=KeyboardM(keyboard, True))

    # Registration of admins
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    #  args -- Arguments
    def reg_admin(self, bot, update, args):
        if args[0] == open('Bot/key.txt').read():
            self.cntrl.upto_librarian(update.message.chat_id)
            bot.send_message(chat_id=update.message.chat_id, text="You have been update to Librarian",
                             reply_markup=KeyboardM(self.keyboard_dict["admin"], True))
            utils.key_gen()

    # Registration of users
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def registration(self, bot, update):
        chat = update.message.chat_id
        self.is_in_reg[chat] = [0, {"id": update.message.chat_id}]
        text_for_message = """
            During registration you have to provide your name, address, phone number and status (student or faculty).\n
            Example:
            Ivan Ivanov,
            ul. Universitetskaya 1, 2-100,
            +71234567890,
            Student     
        """
        bot.send_message(chat_id=chat, text=text_for_message)
        bot.send_message(chat_id=chat, text="Enter your name", reply_markup=KeyboardR([[]]))

    # Steps of the registration
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def reg_steps(self, bot, update):
        chat = update.message.chat_id
        step = self.is_in_reg[chat][0]
        user = self.is_in_reg[chat][1]
        fields = ["name", "address", "phone", "status"]

        if step < len(fields):
            text = update.message.text
            user[fields[step]] = text if text != "Faculty (professor, instructor, TA)" else "Faculty"
            step += 1
            self.is_in_reg[chat][0] += 1
            if step < len(fields):
                keyboard = KeyboardM(self.keyboard_dict["status"], True) if fields[step] == "status" else None
                bot.send_message(chat_id=update.message.chat_id, text="Enter your {}".format(fields[step]),
                                 reply_markup=keyboard)
            else:
                text_for_message = """
                    Check whether all data is correct:
                    Name: {name}
                    Address: {address}
                    Phone: {phone}
                    Status: {status}
                """.format(**user)
                bot.send_message(chat_id=update.message.chat_id, text=text_for_message,
                                 reply_markup=KeyboardM(self.keyboard_dict["reg_confirm"], True))
        elif step == len(fields):
            print(user)
            if update.message.text == "All is correct✅":
                is_incorrect = utils.data_checker(self.is_in_reg[chat][1])
                if is_incorrect[0]:
                    bot.send_message(chat_id=chat, text=is_incorrect[1],
                                     reply_markup=KeyboardM(self.keyboard_dict["unauth"], True))
                else:
                    self.cntrl.registration(user)
                    self.is_in_reg.pop(chat)
                    bot.send_message(chat_id=chat, text="Your request has been sent.\n Wait for librarian confirmation",
                                     reply_markup=KeyboardM(self.keyboard_dict["unconf"], True))
            elif update.message.text == "Something is incorrect❌":
                self.is_in_reg[chat] = [0, {"id": update.message.chat_id}]
                bot.send_message(chat_id=chat, text="Enter your name", reply_markup=KeyboardR([[]]))

    # Main menu of library
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def library(self, bot, update):
        book_handler = MessageHandler(WordFilter('Books📖'), self.cancel)
        article_handler = MessageHandler(WordFilter('Journal Articles📰️'), self.cancel)
        av_handler = MessageHandler(WordFilter('Audio/Video materials📼'), self.cancel)

        self.dispatcher.add_handler(book_handler)
        self.dispatcher.add_handler(article_handler)
        self.dispatcher.add_handler(av_handler)

        bot.send_message(chat_id=update.message.chat_id, text="Choose type of material",
                         reply_markup=KeyboardM(self.keyboard_dict["lib_main"], True))

    # Selected material
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def load_material(self, bot, update):
        pass

    # Cancel the operation
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def cancel(self, bot, update):
        user_id = update.message.chat_id
        if not self.cntrl.chat_exists(user_id):
            keyboard = self.keyboard_dict["unauth"]
        elif self.cntrl.get_user(user_id)['status'] != "librarian":
            keyboard = self.keyboard_dict["auth"]
        else:
            keyboard = self.keyboard_dict["admin"]

        bot.send_message(chat_id=update.message.chat_id, text="Main menu", reply_markup=KeyboardM(keyboard, True))


# Start Bot
# params:
#  Controller -- Bot's data base
def start_bot(controller):
    LibraryBot(configs.token, controller)
