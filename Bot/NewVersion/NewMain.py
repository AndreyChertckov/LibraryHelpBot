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
from datetime import datetime
import logging
import configs


# Class represents a Bot in Telegram
class LibraryBot:
    # Intialization of Bot
    # params:
    # token -- Token from BotFather
    # cntrl -- Bot's data base
    def __init__(self, token, cntrl):
        # Main component
        self.cntrl = cntrl
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        # #
        # Bot's variables
        self.types = func_data.lists["user_types"]
        self.keyboard_dict = func_data.keyboard_dict
        self.location = {}
        self.buffer = {}
        self.flag = {}
        # #
        # Dispatchers
        self.dispatcher.add_handler(CommandHandler('start', self.Main_menu))
        self.dispatcher.add_handler(MHandler(LocationFilter(self.location, None), self.cancel))

        self.dispatcher.add_handler(MHandler(WordFilter('Cancel⤵️'), self.cancel))
        self.dispatcher.add_handler(
            (MHandler((WordFilter('Registration📝') | LocationFilter(self.location, 'Registration📝')) & UserFilter(0),
                      self.Registration)))
        self.dispatcher.add_handler(CommandHandler('get_admin', self.UptoAdmin))

        self.dispatcher.add_handler(
            MHandler(WordFilter('Library🏤') | LocationFilter(self.location, 'Library🏤'), self.library))

        self.dispatcher.add_handler(MHandler(WordFilter('Search🔎'), self.Search))
        self.dispatcher.add_handler(MHandler(WordFilter('My Books📚'), self.MyBooks))
        self.dispatcher.add_handler(MHandler(WordFilter("Check orders🏷") & UserFilter(3), self.CheckOrders))

        self.dispatcher.add_handler(MHandler(WordFilter('Help👤'), self.Help))
        self.dispatcher.add_handler(CallbackQueryHandler(self.call_back))

        self.dispatcher.add_handler(
            (MHandler((WordFilter("Add material🗄") | LocationFilter(self.location, 'Add material🗄')) & UserFilter(3),
                      self.AddMaterial)))
        self.dispatcher.add_handler(
            MHandler((WordFilter("Show users👥") & UserFilter(3)) | LocationFilter(self.location, 'Show users👥'),
                     self.ShowUsers))

        # #
        self.updater.start_polling()
        self.updater.idle()

    # Main menu
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def Main_menu(self, bot, update):
        chat = update.message.chat_id
        user_type = self.cntrl.user_type(chat)
        self.location[chat] = "Main menu"
        self.buffer[chat] = None
        keyboard = [['Library🏤', 'Search🔎', 'My Books📚', 'Help👤']]
        if user_type == 0:  # unauth
            del (keyboard[0][2])
            keyboard = [['Registration📝']] + keyboard
        elif user_type == 3:  # admin
            del (keyboard[0][2])
            keyboard += [["Add material🗄", "Check orders🏷", "Show users👥"]]
        print(update.message)
        bot.send_message(chat_id=update.message.chat_id, text="I'm bot, Hello " + self.types[user_type],
                         reply_markup=RKM(keyboard, True))

    def call_back(self, bot, update):
        key = self.location[update.callback_query.message.chat_id]
        if key == 'Library🏤':
            self.library(bot, update)
        elif key == 'Show users👥':
            self.Users(bot, update)

    # Registration of users
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def Registration(self, bot, update):
        chat = update.message.chat_id
        text = update.message.text
        fields = func_data.lists["reg_fields"]
        if self.location[chat] != 'Registration📝':
            self.location[chat] = 'Registration📝'
            self.buffer[chat] = [0, {'id': chat}]
            bot.send_message(chat_id=chat, text=func_data.sample_messages['reg'])
            bot.send_message(chat_id=chat, text="Enter your name", reply_markup=None)
        elif self.buffer[chat][0] < len(fields):
            step = self.buffer[chat][0]
            user = self.buffer[chat][1]
            user[fields[step]] = text if text != "Faculty (professor, instructor, TA)" else "Faculty"
            self.buffer[chat][1] = user
            self.buffer[chat][0] += 1
            step += 1
            if step < len(fields):
                mes_text = 'Enter your {}'.format(fields[step])
                keyboard = RKM(self.keyboard_dict["status"], True) if fields[step] == "status" else None
            else:
                mes_text = func_data.sample_messages['correctness'].format(**user)
                keyboard = RKM(self.keyboard_dict["reg_confirm"], True)
            bot.send_message(chat_id=chat, text=mes_text, reply_markup=keyboard)
        elif text == "All is correct✅":
            is_incorrect = utils.data_checker(self.buffer[chat][1])
            if is_incorrect[0]:
                bot.send_message(chat_id=chat, text=is_incorrect[1],
                                 reply_markup=None)
                self.Main_menu(bot, update)
            else:
                self.cntrl.registration(self.buffer[chat][1])
                bot.send_message(chat_id=chat, text="Your request has been sent.\n Wait for librarian confirmation",
                                 reply_markup=None)
                self.Main_menu(bot, update)
        elif text == "Something is incorrect❌":
            self.buffer[chat] = [0, {"id": chat}]
            bot.send_message(chat_id=chat, text="Enter your name", reply_markup=None)

    def UptoAdmin(self, bot, update, args):
        if args and args[0] == open('Bot/key.txt').read():
            self.cntrl.upto_librarian(update.message.chat_id)
            bot.send_message(chat_id=update.message.chat_id, text="You have been update to Librarian",
                             reply_markup=None)
            utils.key_gen()
            self.Main_menu(bot, update)

    def library(self, bot, update):
        chat = update.message.chat_id if update.message is not None else update.callback_query.message.chat_id
        text = update.message.text if update.message is not None else update.callback_query.data
        ObjDoc = func_data.lists['book_bd'] + func_data.lists['article_bd'] + func_data.lists['media_bd']
        if self.location[chat] != 'Library🏤':
            self.location[chat] = 'Library🏤'
            self.buffer[chat] = [0, "", None, 0, ""]
            # 0 -- Number of page, 1 -- type of doc, 2 -- doc ,3 -- (0-dont modifier,1-Obj,2-new Obj, 4 -- modifier obj
            bot.send_message(chat_id=chat, text="Choose type of material",
                             reply_markup=RKM(self.keyboard_dict["lib_main"], True))
        elif text in ['Books📖', 'Journal Articles📰', "Audio/Video materials📼"]:
            self.ShowLibrary(bot, update)
        elif text in ObjDoc and self.buffer[chat][3] != 0 or self.buffer[chat][3] == 2:
            self.modifier(bot, update)
        elif update.message == None:
            self.queryWork(bot, update)

    def ShowLibrary(self, bot, update):
        chat = update.message.chat_id if update.message is not None else update.callback_query.message.chat_id
        text = update.message.text if update.message is not None else update.callback_query.data
        doc_type = func_data.analog[text]
        n = 2
        docs = self.cntrl.get_all_doctype(doc_type)
        self.buffer[chat][0] = 0
        self.buffer[chat][1] = doc_type

        if len(docs) == 0:
            bot.send_message(chat_id=chat, text="There are no " + doc_type + " in the library")
            self.Main_menu(bot, update)
            return

        docs = [docs[i * n:(i + 1) * n] for i in range(len(docs) // n + 1) if i * n < len(docs)]
        text_message = ("\n" + "-" * 50 + "\n").join(
            ["{}) {} - {}".format(i + 1, doc['title'], doc["authors"]) for i, doc in enumerate(docs[0])])
        keyboard = [[IKB(str(i + 1), callback_data=str(i)) for i in range(len(docs[0]))]]
        keyboard += [[IKB("⬅", callback_data='prev'), IKB("➡️", callback_data='next')]]
        update.message.reply_text(text=text_message + "\nCurrent page: {}/{}".format(str(1), len(docs)),
                                  reply_markup=IKM(keyboard))

    def queryWork(self, bot, update):

        chat = update.message.chat_id if update.message is not None else update.callback_query.message.chat_id
        query = update.callback_query
        print(query.data)
        doc_type = self.buffer[chat][1]
        n = 2
        docs = self.cntrl.get_all_doctype(doc_type)
        docs = [docs[i * n:(i + 1) * n] for i in range(len(docs) // n + 1) if i * n < len(docs)]
        max_page = len(docs)
        if (query.data in ["prev", "next", 'cancel']) and (max_page or query.data == 'cancel'):
            if query.data == "next":
                self.buffer[chat][0] = (self.buffer[chat][0] + 1) % max_page
            if query.data == "prev":
                self.buffer[chat][0] = (self.buffer[chat][0] - 1) % max_page

            text_message = ("\n" + "-" * 50 + "\n").join(
                ["{}) {} - {}".format(i + 1, doc['title'], doc["authors"]) for i, doc in
                 enumerate(docs[self.buffer[chat][0]])])
            keyboard = [[IKB(str(i + 1), callback_data=str(i)) for i in range(len(docs[self.buffer[chat][0]]))]]
            keyboard += [[IKB("⬅", callback_data='prev'), IKB("➡️", callback_data='next')]]
            bot.edit_message_text(text=text_message + "\nCurrent page: " + str(self.buffer[chat][0] + 1),
                                  chat_id=chat,
                                  message_id=query.message.message_id, reply_markup=IKM(keyboard))
        elif utils.is_int(query.data):
            k = int(query.data)
            doc = docs[self.buffer[chat][0]][k]
            text = """Title: {title};\nAuthors: {authors}\n"""
            if doc_type == "book":
                text += """Description: {description}\nFree copy: {free_count}"""
            elif doc_type == "article":
                text += """Journal: {journal}\nIssue: {issue}\nDate: {date}\nFree copy: {free_count}"""
            elif doc_type == "media":
                text += """Free copy: {free_count}"""
            print(doc)
            text = text.format(**doc)
            type = self.cntrl.user_type(chat)
            keyboard = [[]]
            if type == 2:
                keyboard += [[IKB("Order the book", callback_data='order ' + query.data)]]
            elif type == 3:
                keyboard += [[IKB("Modifier", callback_data='update ' + query.data)]]
            keyboard += [[IKB("Cancel", callback_data='cancel')]]
            bot.edit_message_text(text=text, chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))
        elif query.data.split(" ")[0] == 'order':
            k = int(query.data.split(" ")[1])
            doc = docs[self.buffer[chat][0]][k]
            print(doc)
            status, report = self.cntrl.check_out_doc(chat, doc['id'], type_bd=doc_type)
            message = "Your order was successful.\nCollect the book from the library not later than 4 hours" if status else "You already have this document"
            bot.edit_message_text(text=message, chat_id=chat, message_id=query.message.message_id)

        elif query.data.split(' ')[0] == 'update':

            k = int(query.data.split(" ")[1])
            self.buffer[chat][2] = docs[self.buffer[chat][0]][k]
            self.buffer[chat][3] = 1
            text = """"Choose modified parameters:\n"""
            list_bd = func_data.lists
            if doc_type == "book":
                list_bd = list_bd['book_bd']
            elif doc_type == "article":
                list_bd = list_bd['article_bd']
            elif doc_type == "media":
                list_bd = list_bd['media_bd']
            list_bd = list_bd[:len(list_bd) - 1]
            for i in range(len(list_bd)):
                text += '\n' + str(i + 1) + " - " + list_bd[i]
            keyboard = [
                [IKB(list_bd[i + j * 3], callback_data=list_bd[i + j * 3]) for i in range(min(3, len(list_bd) - j * 3))
                 ] for j in range(len(list_bd) // 3 + (1 if len(list_bd) % 3 > 0 else 0))]
            keyboard += [[IKB("Cancel", callback_data='cancel')]]
            bot.edit_message_text(text=text, chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))

    def modifier(self, bot, update):
        chat = update.message.chat_id if update.message is not None else update.callback_query.message.chat_id
        text = update.message.text if update.message is not None else update.callback_query.data
        if self.buffer[chat][3] == 1:
            self.buffer[chat][3] = 2
            self.buffer[chat][4] = text
            mes_text = 'Enter new {}.\nOld value - {}.'.format(text, self.buffer[chat][2][text])
            keyboard = [[IKB("Cancel", callback_data='cancel')]]
            bot.edit_message_text(text=mes_text, chat_id=chat, message_id=update.callback_query.message.message_id,
                                  reply_markup=IKM(keyboard))
        elif self.buffer[chat][3] == 2:
            self.buffer[chat][3] = 1
            if text != 'cancel':
                self.buffer[chat][2][self.buffer[chat][4]] = update.message.text
                self.cntrl.modify_document(self.buffer[chat][2], self.buffer[chat][1])
                bot.send_message(chat_id=chat, text="Updated.")
            else:
                bot.send_message(chat_id=chat, text='Cancel')

    def Search(self, bot, update):
        pass

    def MyBooks(self, bot, update):
        chat = update.message.chat_id
        orders = self.cntrl.get_user_orders(chat)
        print(orders)
        orders = ("\n" + "-" * 50 + "\n").join(
            ["{}) {} written by {}\n Available till {}".format(i + 1, doc['doc_dict']['title'],
                                                               doc['doc_dict']['authors'], doc['time_out']) for
             i, doc in
             enumerate(orders)])
        bot.send_message(text=orders, chat_id=chat,  reply_markup=None)

    def Help(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="If you have any question, you can wtite to @Sermark.")

    def AddMaterial(self, bot, update):
        chat = update.message.chat_id if update.message is not None else update.callback_query.message.chat_id
        text = update.message.text if update.message is not None else update.callback_query.data

        if self.location[chat] != 'Add material🗄':
            self.location[chat] = 'Add material🗄'
            self.buffer[chat] = [0, None, {}]
            # 0 -- Number of page, 1 -- type of doc, 2 -- doc
            bot.send_message(chat_id=chat, text="Choose type of material",
                             reply_markup=RKM(self.keyboard_dict["lib_main"], True))
        elif (text in ['Books📖', 'Journal Articles📰', "Audio/Video materials📼"]) and self.buffer[chat][1] == None:
            self.buffer[chat][1] = func_data.analog[text]
            self.buffer[chat][0] = 0
            bot.send_message(chat_id=chat, text="Enter title:", reply_markup=RKM([[]]))
        elif self.buffer[chat][0] < len(func_data.lists[self.buffer[chat][1] + '_bd']) - 1:
            step = self.buffer[chat][0]
            listAn = func_data.lists[self.buffer[chat][1] + '_bd']
            listAn = listAn[:len(listAn) - 1]
            listText = func_data.lists[self.buffer[chat][1]]
            doc = self.buffer[chat][2]
            doc[listAn[step]] = text
            step += 1
            if step < len(listAn):
                keyboard = [[]]
                mes_text = 'Enter {}'.format(listText[step])
            else:
                keyboard = func_data.keyboard_dict['reg_confirm']
                mes_text = func_data.sample_messages['correctness_' + self.buffer[chat][1]].format(**doc)
            self.buffer[chat][0] = step
            self.buffer[chat][2] = doc
            bot.send_message(chat_id=chat, text=mes_text, reply_markup=RKM(keyboard, True))
        elif text in func_data.keyboard_dict['reg_confirm'][0]:
            if text == 'All is correct✅':
                self.cntrl.add_document(self.buffer[chat][2], self.buffer[chat][1])
                bot.send_message(chat_id=chat, text='Document was added.', reply_markup=None)
                self.cancel(bot, update)
            else:
                self.location[chat] = 'Main menu'
                self.AddMaterial(bot, update)
        print(self.buffer[chat])

    def CheckOrders(self, bot, update):
        pass

    def ShowUsers(self, bot, update):

        chat = update.message.chat_id if update.message is not None else update.callback_query.message.chat_id
        text = update.message.text if update.message is not None else update.callback_query.data
        print(text)
        if self.location[chat] != 'Show users👥':
            self.location[chat] = 'Show users👥'
            self.buffer[chat] = [0, 'conf/unconf', None, '']
            keyboard = [['Users🔎', "Unconfirm users👥", 'Cancel⤵️']]
            bot.send_message(chat_id=update.message.chat_id, text="Choose option", reply_markup=RKM(keyboard, True))
        elif text in ['Users🔎', "Unconfirm users👥"]:
            self.location[chat] = 'Show users👥'
            n = 3
            if text == "Unconfirm users👥":
                patrons = self.cntrl.get_all_unconfirmed()
                self.buffer[chat][1] = 'unconf'
            else:
                patrons = self.cntrl.get_all_patrons()
                self.buffer[chat][1] = 'conf'
            if len(patrons) == 0:
                bot.send_message(chat_id=chat, text="There are no users")
                return
            patrons = [patrons[i * n:(i + 1) * n] for i in range(len(patrons) // n + 1) if i * n < len(patrons)]
            if not (chat in self.buffer):
                self.buffer[chat][0] = 0
            text_message = ("\n" + "-" * 50 + "\n").join(
                ["{}) {} - {}".format(i + 1, user['name'], user["status"]) for i, user in enumerate(patrons[0])])
            keyboard = [[IKB(str(i + 1), callback_data=str(i)) for i in range(len(patrons[0]))]]
            keyboard += [[IKB("⬅", callback_data='prev'), IKB("➡️", callback_data='next')]]
            update.message.reply_text(text=text_message + "\nCurrent page: " + str(1), reply_markup=IKM(keyboard))
        elif self.buffer[chat][3].split(' ')[0] == 'edit':
            params = dict(zip(['e1', 'e2', 'e3', 'e4'], func_data.lists["reg_fields"]))
            user = self.buffer[chat][2]
            user[params[self.buffer[chat][3].split(' ')[1]]] = text
            self.cntrl.modify_user(user)
            bot.send_message(chat_id=chat, text="Update", reply_markup=None)
        elif self.buffer[chat][3].split(' ')[0] == 'notice':
            chat_id = self.buffer[chat][3].split(' ')[1]
            bot.send_message(chat_id=chat_id, text="From librarian:\n" + text, reply_markup=None)

    def Users(self, bot, update):

        query = update.callback_query
        chat = query.message.chat_id
        n = 3
        if self.buffer[chat][1] == 'unconf':
            patrons = self.cntrl.get_all_unconfirmed()
        else:
            patrons = self.cntrl.get_all_patrons()
        patrons = [patrons[i * n:(i + 1) * n] for i in range(len(patrons) // n + 1) if i * n < len(patrons)]
        max_page = len(patrons)
        if (query.data in ["prev", "next", 'cancel']) and (max_page or query.data == 'cancel'):
            self.buffer[chat][3] = ''
            if query.data == "next":
                self.buffer[chat][0] = (self.buffer[chat][0] + 1) % max_page
            if query.data == "prev":
                self.buffer[chat][0] = (self.buffer[chat][0] - 1) % max_page

            text_message = ("\n" + "-" * 50 + "\n").join(
                ["{}) {} - {}".format(i + 1, user['name'], user["status"]) for i, user in
                 enumerate(patrons[self.buffer[chat][0]])])
            keyboard = [[IKB(str(i + 1), callback_data=str(i)) for i in range(len(patrons[self.buffer[chat][0]]))]]
            keyboard += [[IKB("⬅", callback_data='prev'), IKB("➡️", callback_data='next')]]
            bot.edit_message_text(text=text_message + "\nCurrent page: " + str(self.buffer[chat][0] + 1), chat_id=chat,
                                  message_id=query.message.message_id, reply_markup=IKM(keyboard))
        elif utils.is_int(query.data):
            k = int(query.data)
            user = patrons[self.buffer[chat][0]][k]
            self.buffer[chat][2] = user
            if self.buffer[chat][1] == 'conf':
                user_id = user['id']
                orders = self.cntrl.get_user_orders(user_id)
                text = """
                            Name: {name}\nAddress: {address}\nPhone: {phone}\nStatus: {status}\nTaken documents: """.format(
                    **user)
                text += "{}\nOverdue documents: ".format(len(orders))
                text += str(len([i for i in orders if datetime.strptime(i['time_out'], "%Y-%m-%d") < datetime.today()]))
                keyboard = [[IKB("Edit", callback_data='edit'), IKB("Cancel", callback_data='cancel')]]
                if orders:
                    keyboard[0].insert(1, IKB("Orders", callback_data='order'))
                else:
                    keyboard[0].insert(1, IKB("Delete", callback_data='delete'))
            else:
                text = """
                            Check whether all data is correct:\nName: {name}\nAddress: {address}\nPhone: {phone}\nStatus: {status}
                            """.format(**user)
                keyboard = [[IKB("Apply✅", callback_data='apply ' + query.data),
                             IKB('Reject❌', callback_data='reject ' + query.data)],
                            [IKB("Cancel", callback_data='cancel')]]
            bot.edit_message_text(text=text, chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))
        elif query.data.split(' ')[0] in ['apply', 'reject']:
            k = int(query.data.split(" ")[1])
            user_id = patrons[self.buffer[chat][0]][k]["id"]
            if query.data.split(' ')[0] == 'apply':
                self.cntrl.confirm_user(user_id)
                bot.edit_message_text(text="This user was confirmed", chat_id=chat, message_id=query.message.message_id)
                bot.send_message(chat_id=user_id,
                                 text="Your application was confirmed. Send /start for update functions",
                                 reply_markup=None)
            else:
                self.cntrl.delete_user(user_id)
                bot.edit_message_text(text="This user was rejected", chat_id=chat, message_id=query.message.message_id)
                bot.send_message(chat_id=user_id, text="Your application was rejected",
                                 reply_markup=None)
        elif query.data == 'edit':
            keyboard = [[IKB("Name", callback_data='e1'), IKB("Phone", callback_data='e3')],
                        [IKB("Address", callback_data='e2'), IKB("Status", callback_data='e4')],
                        [IKB("Cancel", callback_data='cancel')]]
            text = "Choose edited parameter or press cancel"
            bot.edit_message_text(text=text, chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))
        elif query.data in ['e1', 'e2', 'e3', 'e4']:
            user = self.buffer[chat][2]
            self.buffer[chat][3] = 'edit ' + query.data
            keyboard = [[IKB("Cancel", callback_data='cancel')]]
            params = dict(zip(['e1', 'e2', 'e3', 'e4'], func_data.lists["reg_fields"]))
            text = 'Enter new {}.\nOld value - {}.'.format(params[query.data], user[params[query.data]])
            bot.edit_message_text(text=text, chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))
        elif query.data == 'delete':
            self.cntrl.delete_user(self.buffer[chat][2]['id'])
            text = "User card has been deleted"
            bot.edit_message_text(text=text, chat_id=chat, message_id=query.message.message_id)
        elif query.data == 'order':
            user_id = self.buffer[chat][2]['id']
            orders = self.cntrl.get_user_orders(user_id)
            # print(orders)
            keyboard = [[IKB(str(i + 1), callback_data='order ' + str(i)) for i in range(len(orders))]]
            self.buffer[chat][3] = orders
            orders = ("\n" + "-" * 50 + "\n").join(
                ["{}) {} written by {}\n Available till {}".format(i + 1, doc['doc_dict']['title'],
                                                                   doc['doc_dict']['authors'], doc['time_out']) for
                 i, doc in
                 enumerate(orders)])
            keyboard += [[IKB("Cancel", callback_data='cancel')]]
            bot.edit_message_text(text=orders, chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))
        elif query.data.split(" ")[0] == 'order' and utils.is_int(query.data.split(" ")[1]):
            user = self.buffer[chat][2]
            user_id = user['id']
            doc, time, time_out = self.buffer[chat][3][int(query.data.split(" ")[1])].values()
            text = "User name: {name}\nPhone: {phone}\nStatus: {status}\n\n".format(**user)
            text += "Document title: {title}\nAuthors: {authors}\n\n".format(**doc)
            text += "Date of taking: {}\nDate of returning: {}".format(time, time_out)
            keyboard = [[IKB("Book return", callback_data='return ' + query.data.split(" ")[1]),
                         IKB("Send notification", callback_data='notice'),
                         IKB("Cancel", callback_data='cancel')]]
            bot.edit_message_text(text=text, chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))
        elif query.data == 'notice':
            keyboard = [[IKB("Cancel", callback_data='cancel')]]
            user = self.buffer[chat][2]
            user_id = user['id']
            self.buffer[chat][3] = 'notice ' + user_id
            text = "Enter message to user"
            bot.edit_message_text(text=text, chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))
        elif query.data.split(" ")[0] == 'return':
            doc, time, time_out = self.buffer[chat][3][int(query.data.split(" ")[1])].values()
            self.cntrl.return_doc(doc)
            keyboard = [[IKB("Return to the list", callback_data='cancel')]]

            bot.edit_message_text(text='Document was returned', chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))

    def cancel(self, bot, update):
        print("Cancel")
        self.buffer[update.message.chat_id] = None
        self.Main_menu(bot, update)


# Start Bot
# params:
#  Controller -- Bot's data base
def start_bot(controller):
    construct(LibraryBot)
    LibraryBot(configs.token, controller)
