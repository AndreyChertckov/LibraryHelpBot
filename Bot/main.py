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
        # self.logger = logging.getLogger(__name__)
        self.keyboard_dict = func_data.keyboard_dict
        self.types = func_data.lists["user_types"]
        self.is_in_reg = {}
        self.admins = {}
        self.is_adding = {}

        self.add_user_handlers()
        self.add_admin_handlers()
        start_handler = CommandHandler('start', self.start)

        self.dispatcher.add_handler(start_handler)
        # self.dispatcher.add_error_handler(self.error)

        self.updater.start_polling()
        self.updater.idle()

    def add_user_handlers(self):
        reg_handler = MHandler(WordFilter('Registration📝') & UserFilter(0), self.registration)
        reg_step_handler = MHandler(StateFilter(self.is_in_reg) & Filters.text, self.reg_steps)
        reg_admin_handler = CommandHandler('get_admin', self.reg_admin, filters=UserFilter(2), pass_args=True)
        library_handler = MHandler(WordFilter('Library🏤'), self.library)
        cancel_handler = MHandler(WordFilter('Cancel⤵️'), self.cancel)

        book_handler = MHandler(WordFilter('Books📖') & UserFilter(3, True), self.cancel)
        article_handler = MHandler(WordFilter('Journal Articles📰') & UserFilter(3, True), self.cancel)
        av_handler = MHandler(WordFilter('Audio/Video materials📼') & UserFilter(3, True), self.cancel)

        self.dispatcher.add_handler(book_handler)
        self.dispatcher.add_handler(article_handler)
        self.dispatcher.add_handler(av_handler)
        self.dispatcher.add_handler(reg_handler)
        self.dispatcher.add_handler(reg_step_handler)
        self.dispatcher.add_handler(reg_admin_handler)
        self.dispatcher.add_handler(library_handler)
        self.dispatcher.add_handler(cancel_handler)

    def add_admin_handlers(self):
        self.dispatcher.add_handler(CommandHandler('get_key', utils.get_key, filters=UserFilter(3)))
        self.dispatcher.add_handler(MHandler(WordFilter("User management👥") & UserFilter(3), self.user_manage))
        self.dispatcher.add_handler(
            MHandler(WordFilter("Material management📚") & UserFilter(3), self.mat_manage))
        self.dispatcher.add_handler(CallbackQueryHandler(self.conf_user))

        doc_type = lambda key: lambda bot, update: self.start_adding(bot, update, key)
        self.dispatcher.add_handler(MHandler(WordFilter('Books📖') & UserFilter(3), doc_type("book")))
        self.dispatcher.add_handler(MHandler(WordFilter('Journal Articles📰') & UserFilter(3), doc_type('article')))
        self.dispatcher.add_handler(MHandler(WordFilter('Audio/Video materials📼') & UserFilter(3), doc_type('media')))
        self.dispatcher.add_handler(MHandler(StateFilter(self.is_adding) & Filters.text, self.adding_steps))

        self.dispatcher.add_handler(MHandler(WordFilter("Add material🗄") & UserFilter(3), self.add_doc))
        self.dispatcher.add_handler(MHandler(WordFilter("Search🔎") & UserFilter(3), self.cancel))

    # Main menu
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def start(self, bot, update):
        user_type = self.cntrl.user_type(update.message.chat_id)
        keyboard = self.keyboard_dict[self.types[user_type]]

        bot.send_message(chat_id=update.message.chat_id, text="I'm bot, Hello",
                         reply_markup=RKM(keyboard, True))

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
            print(user)
            if update.message.text == "All is correct✅":
                is_incorrect = utils.data_checker(self.is_in_reg[chat][1])
                if is_incorrect[0]:
                    bot.send_message(chat_id=chat, text=is_incorrect[1],
                                     reply_markup=RKM(self.keyboard_dict["unauth"], True))
                else:
                    self.cntrl.registration(user)
                    self.is_in_reg.pop(chat)
                    bot.send_message(chat_id=chat, text="Your request has been sent.\n Wait for librarian confirmation",
                                     reply_markup=RKM(self.keyboard_dict["unconf"], True))
            elif update.message.text == "Something is incorrect❌":
                self.is_in_reg[chat] = [0, {"id": update.message.chat_id}]
                bot.send_message(chat_id=chat, text="Enter your name", reply_markup=RKR([[]]))

    def user_manage(self, bot, update):
        keyboard = self.keyboard_dict["user_management"]
        bot.send_message(chat_id=update.message.chat_id, text="Choose option",
                         reply_markup=RKM(keyboard, True))
        self.dispatcher.add_handler(MHandler(WordFilter("Confirm application📝") & UserFilter(3), self.confirm))
        self.dispatcher.add_handler(MHandler(WordFilter("Check overdue📋") & UserFilter(3), self.cancel))
        self.dispatcher.add_handler(MHandler(WordFilter("Show users👥") & UserFilter(3), self.cancel))

    def confirm(self, bot, update):
        chat = update.message.chat_id
        n = 3
        unconf_users = self.cntrl.get_all_unconfirmed()
        if len(unconf_users) == 0:
            bot.send_message(chat_id=chat, text="There are no application to confirm")
            return
        unconf_users = [unconf_users[i * n:(i + 1) * n] for i in range(len(unconf_users) // n + 1)]
        if not (chat in self.admins):
            self.admins[chat] = 0
        text_message = ("\n" + "-" * 50 + "\n").join(
            ["{}) {} - {}".format(i + 1, user['name'], user["status"]) for i, user in enumerate(unconf_users[0])])
        keyboard = [[IKB(str(i + 1), callback_data=str(i)) for i in range(len(unconf_users[0]))]]
        keyboard += [[IKB("⬅", callback_data='next'), IKB("➡️", callback_data='next')]]
        update.message.reply_text(text=text_message + "\nCurrent page: " + str(1), reply_markup=IKM(keyboard))

    def conf_user(self, bot, update):
        query = update.callback_query
        chat = query.message.chat_id
        n = 3
        unconf_users = self.cntrl.get_all_unconfirmed()
        unconf_users = [unconf_users[i * n:(i + 1) * n] for i in range(len(unconf_users) // n + 1)]
        max_page = len(unconf_users) - 1
        if (query.data == "prev" or "next" == query.data) and max_page:
            if query.data == "next":
                if self.admins[chat] == max_page:
                    self.admins[chat] = 0
                else:
                    self.admins[chat] += 1
            if query.data == "prev":
                if self.admins[chat] == 0:
                    self.admins[chat] = max_page
                else:
                    self.admins[chat] -= 1

            text_message = ("\n" + "-" * 50 + "\n").join(
                ["{}) {} - {}".format(i + 1, user['name'], user["status"]) for i, user in
                 enumerate(unconf_users[self.admins[chat]])])
            keyboard = [[IKB(str(i + 1), callback_data=str(i)) for i in range(len(unconf_users[self.admins[chat]]))]]
            keyboard += [[IKB("⬅", callback_data='prev'), IKB("➡️", callback_data='next')]]
            bot.edit_message_text(text=text_message + "\nCurrent page: " + str(self.admins[chat] + 1), chat_id=chat,
                                  message_id=query.message.message_id, reply_markup=IKM(keyboard))
        elif utils.is_int(query.data):
            k = int(query.data)
            user = unconf_users[self.admins[chat]][k]
            text = """
            Check whether all data is correct:\nName: {name}\nAddress: {address}\nPhone: {phone}\nStatus: {status}
            """.format(**user)
            keyboard = [[IKB("Accept✅", callback_data='accept ' + query.data),
                         IKB("Reject️❌", callback_data='reject ' + query.data)]]
            bot.edit_message_text(text=text, chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))
        elif query.data.split(" ")[0] == 'accept':
            k = int(query.data.split(" ")[1])
            user_id = unconf_users[self.admins[chat]][k]["id"]
            self.cntrl.confirm_user(user_id)
            bot.edit_message_text(text="This user was confirmed", chat_id=chat, message_id=query.message.message_id)
            bot.send_message(chat_id=user_id, text="Your application was confirmed",
                             reply_markup=RKM(self.keyboard_dict[self.types[2]], True))
        elif query.data.split(" ")[0] == 'reject':
            k = int(query.data.split(" ")[1])
            user_id = unconf_users[self.admins[chat]][k]["id"]
            self.cntrl.delete_user(user_id)
            bot.edit_message_text(text="This user was rejected", chat_id=chat, message_id=query.message.message_id)
            bot.send_message(chat_id=user_id, text="Your application was rejected",
                             reply_markup=RKM(self.keyboard_dict[self.types[0]], True))

    def check_overdue(self, bot, update):
        pass

    def show_users(self, bot, update):
        pass

    def mat_manage(self, bot, update):
        reply_markup = RKM(self.keyboard_dict["mat_management"], True)
        bot.send_message(chat_id=update.message.chat_id, text="Choose option", reply_markup=reply_markup)

    def add_doc(self, bot, update):
        reply_markup = RKM(self.keyboard_dict["lib_main"], True)
        bot.send_message(chat_id=update.message.chat_id, text="Choose type of material", reply_markup=reply_markup)

    def start_adding(self, bot, update, key):
        chat = update.message.chat_id
        self.is_adding[chat] = [0, {"id": utils.randint()}, key]
        bot.send_message(chat_id=chat, text=func_data.sample_messages[key])
        bot.send_message(chat_id=chat, text="Enter title", reply_markup=RKR([[]]))

    # Steps of the material addition
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def adding_steps(self, bot, update):
        chat = update.message.chat_id
        step = self.is_adding[chat][0]
        doc = self.is_adding[chat][1]
        key = self.is_adding[chat][2]
        fields = func_data.lists[key + "_bd"]

        if step < len(fields):
            text = update.message.text
            doc[fields[step]] = int(text) if utils.is_int(text) else text
            step += 1
            self.is_adding[chat][0] += 1
            if step < len(fields):
                bot.send_message(chat_id=update.message.chat_id, text="Enter {}".format(fields[step]))
            else:
                text_for_message = func_data.sample_messages['correctness_' + key].format(**doc)
                bot.send_message(chat_id=update.message.chat_id, text=text_for_message,
                                 reply_markup=RKM(self.keyboard_dict["reg_confirm"], True))
        elif step == len(fields):
            print(doc)
            if update.message.text == "All is correct✅":
                # self.cntrl.add_document(doc, key) нужный метод
                self.is_adding.pop(chat)
                bot.send_message(chat_id=chat, text="Document has been added",
                                 reply_markup=RKM(self.keyboard_dict["admin"], True))
            elif update.message.text == "Something is incorrect❌":
                self.is_adding[chat] = [0, {"id": update.message.chat_id}]
                bot.send_message(chat_id=chat, text="Enter your name", reply_markup=RKR([[]]))

    # Main menu of library
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def library(self, bot, update):

        bot.send_message(chat_id=update.message.chat_id, text="Choose type of material",
                         reply_markup=RKM(self.keyboard_dict["lib_main"], True))

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
        user_type = self.cntrl.user_type(update.message.chat_id)
        keyboard = self.keyboard_dict[self.types[user_type]]

        bot.send_message(chat_id=update.message.chat_id, text="Main menu", reply_markup=RKM(keyboard, True))

    def error(self, bot, update, error):
        """Log Errors caused by Updates."""
        self.logger.warning('Update "%s" caused error "%s"', update, error)


# Start Bot
# params:
#  Controller -- Bot's data base
def start_bot(controller):
    LibraryBot(configs.token, controller)
