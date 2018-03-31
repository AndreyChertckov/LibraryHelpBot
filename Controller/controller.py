import logging
from datetime import datetime, timedelta

from DataBase.DBmanager import Manager
from DataBase.DBPackager import Packager


# Class booking system
class Controller:
    def __init__(
            self, lc=False, lf=False, file_log='controller.log', test_logging=False,
            name_test='0'):
        self.DBmanager = Manager()
        self.is_log = False
        if lc or lf:
            self.is_log = True
            logger_str = 'controller' if not test_logging else 'controller_' + name_test
            self.logger = logging.getLogger(logger_str)
            self.logger.setLevel(logging.DEBUG)
            formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            if lc:
                ch = logging.StreamHandler()
                ch.setLevel(logging.INFO)
                ch.setFormatter(formater)
                self.logger.addHandler(ch)
            if lf:
                fh = logging.FileHandler(file_log)
                fh.setLevel(logging.INFO)
                fh.setFormatter(formater)
                self.logger.addHandler(fh)
        self.log('INFO', 'Start work.')

    def log(self, type_msg, msg):
        if self.is_log:
            if type_msg == 'WARNING':
                self.logger.warning(msg)
            elif type_msg == 'INFO':
                self.logger.info(msg)

    # Put user in queue for accepting to the library
    # param: user_info: dictionary {id,name,address,status,phone}
    def registration(self, user_info):
        self.DBmanager.add_unconfirmed(Packager(user_info))
        self.log('INFO', 'User {} signed up. Whaiting for librarians confirmation.'.format(user_info['name']))

    # Accept user to the library
    # param: user_id - id of user
    def confirm_user(self, user_id, librarian_id=-1):
        user = self.get_user(user_id)
        if not user:
            return False
        user['history'] = str([])
        user['current_docs'] = str([])
        self.delete_user(user_id)
        self.DBmanager.add_patron(Packager(user))
        by_who = 'UNKNOW' if librarian_id == -1 else self.get_user(librarian_id)['name']
        self.log('INFO', 'User status {} is confirmed by {}.'.format(user['name'], by_who))
        return True

    # Move patron from table patrons to table librarians
    # param: user_id : id of user
    def upto_librarian(self, user_id):
        user_info = self.get_user(user_id)
        user_info.pop('current_docs', 0)
        user_info.pop('history', 0)
        self.delete_user(user_id)
        self.DBmanager.add_librarian(Packager(user_info))
        self.log('INFO', 'User {} is upgraded to librarian'.format(user_info['name']))

    def modify_user(self, new_user_info, by_who_id=0):
        user_id = new_user_info['id']
        self.DBmanager.edit_label('patrons', list(new_user_info.keys()), list(new_user_info.values()), user_id)
        by_who = 'UNKNOW' if by_who_id == 0 else self.get_user(by_who_id)['name']
        log = 'User with id {} was modified by {}: '.format(
            user_id, by_who) + ', '.join(
            ['new ' + str(key) + ' is ' + str(new_user_info[key]) for key in new_user_info.keys()])
        self.log('INFO', log)

    # Delete user by user_info
    # param: user_info: dictionary {id,name,address,status,phone}
    def delete_user(self, user_id):
        table = ['unauthorized', 'unconfirmed', 'patrons', 'librarians'][self.user_type(user_id)]
        if table != 'unauthorized':
            u_name = self.get_user(user_id)['name']
            self.DBmanager.delete_label(table, user_id)
            self.log('INFO', 'User {} is deleted from table {}.'.format(u_name, table))

    # Return all users who don`t confirmed
    def get_all_unconfirmed(self):
        rows = self.DBmanager.select_all("unconfirmed")
        return [{'id': user[0], 'name': user[1], 'phone': user[2], 'address': user[3], 'status': user[4]} for user in
                rows]

    # По-другому чет не работает
    # ToDo: исправить костыль
    def get_patron(self, patron_id):
        patrons = self.get_all_patrons()
        for i in patrons:
            if (i['id'] == patron_id):
                return i

    # Return all patrons from database
    def get_all_patrons(self, by_who_id=-1):
        rows = self.DBmanager.select_all("patrons")
        by_who = 'UNKNOW' if by_who_id == -1 else self.get_user(by_who_id)['name']
        self.log('INFO', 'Get all patrons by {}'.format(by_who))
        return [dict(zip(['id', 'name', 'phone', 'address', 'history', 'current_docs', 'status', 'queue'], user)) for
                user in
                rows]

    # Return all librarians from database
    def get_all_librarians(self, by_who_id=-1):
        by_who = 'UNKNOW' if by_who_id == -1 else self.get_user(by_who_id)['name']
        self.log('INFO', 'Get all librarians by {}'.format(by_who))
        rows = self.DBmanager.select_all("librarians")
        return [{'id': user[0], 'name': user[1], 'phone': user[2], 'address': user[3]} for user in
                rows]

    # Return true if chat with user exist, false if not
    # param : user_id - id of user
    # return : bool value
    def chat_exists(self, user_id):
        return any(
            [self.DBmanager.select_label('librarians', user_id), self.DBmanager.select_label('patrons', user_id)])

    # Return user by id
    # param : user_id - id of user
    # return : dictionary user {id,name,address,phone,status} if user librarian or unconfirmed,
    # or {id,name,address,phone,history,current_docs,status},
    # or false if user doesn`t existе
    def get_user(self, user_id):
        keys = ['id', 'name']
        status = self.user_type(user_id)
        user = {}
        user_db = None
        if status == 2:
            user_db = self.DBmanager.select_label('patrons', user_id)
            keys.extend(['phone', 'address','history', 'current_docs', 'status'])
        elif status == 3:
            user_db = self.DBmanager.select_label('librarians', user_id)
            keys.extend(['phone', 'address'])
        elif status == 1:
            user_db = self.DBmanager.select_label('unconfirmed', user_id)
            keys.extend(['phone', 'address', 'status'])
        else:
            self.log('WARNING', 'User with id {} not found.'.format(user_id))
            return False
        return dict(zip(keys, user_db))

    # Returns in which table the user is located
    # param : user_id - id of user
    # return : if 0 then user is unauthorized
    #          if 1 then user is unconfirmed
    #          if 2 then user is patron
    #          if 3 then user is admin
    def user_type(self, user_id):
        d = {"unauthorized": 0, 'unconfirmed': 1, 'patron': 2, 'admin': 3}
        if self.DBmanager.select_label('librarians', user_id):
            return d['admin']
        elif self.DBmanager.select_label('patrons', user_id):
            return d['patron']
        elif self.DBmanager.select_label('unconfirmed', user_id):
            return d['unconfirmed']
        else:
            return d['unauthorized']

    def add_queue_order(self, user_id, type_of_media, doc_id):
        status = self.DBmanager.get_label('status', 'patrons', user_id)
        if (status == 'Student'):
            priority = 0
        elif (status == 'Instructor'):
            priority = 1
        elif (status == 'TA'):
            priority = 2
        elif (status == 'VP'):
            priority = 3
        else:
            priority = 4
        mas = eval(self.DBmanager.get_label('queue', type_of_media, doc_id))
        if (mas[priority].__contains__(user_id)):
            return
        mas[priority] += [user_id]
        self.DBmanager.edit_label(type_of_media, ['queue'], [str(mas)], doc_id)
        queue = eval(self.DBmanager.get_label('queue', 'patrons', user_id))
        queue += [doc_id]
        self.DBmanager.edit_label('patrons', ['queue'], [str(queue)], user_id)

    def get_user_queue(self, user_id):
        queue = eval(self.DBmanager.get_label('queue', 'patrons', user_id))
        return queue

    def renew_item(self, user_id, doc_type, doc_id):
        user = self.get_user(user_id)
        orders_id = eval(user['current_docs'])
        returning_time=self.get_returning_time(0,doc_type,doc_id,user_id)
        for id in orders_id:
            order=self.get_order(id)
            if (order['table'] == doc_type and
                   order['doc_id'] == doc_id
                    and order['renewed'] == 0):
                self.DBmanager.edit_label('orders', ['out_of_time','renewed'],
                                          [str(datetime.now()+timedelta(weeks=returning_time)),1],id)


    def get_user_by_name(self, name, by_who_id=-1):
        by_who = 'UNKNOW' if by_who_id == -1 else self.get_user(by_who_id)
        user = self.DBmanager.get_by('name', 'patrons', name)[0]
        self.log('INFO', 'Get user with name {} by {}'.format(name, by_who))
        return dict(zip(['id', 'name', 'phone', 'address', 'history', 'current_docs', 'status'], user))

    # Check out book
    # param : user_id - id of user
    # param : book_id - id of book
    def get_returning_time(self,returning_time,type_bd,doc_id,user_id):
        user_status = self.DBmanager.get_label('status', 'patrons', user_id)
        if returning_time == 0 and type_bd == 'book':
            is_best_seller = self.DBmanager.get_label('best_seller', type_bd, doc_id) == 1
            returning_time = 3 if user_status == 'Student' else 4
            returning_time = 2 if is_best_seller else returning_time
        elif type_bd != 'book':
            returning_time = 2
        returning_time = 1 if user_status == 'VP' else returning_time
        return returning_time

    def check_out_doc(self, user_id, doc_id, type_bd='book', returning_time=0, date_when_took=datetime.now()):

        if self.DBmanager.select_label(type_bd, doc_id) == None:
            self.log('WARNING', 'Document with id {} not found.'.format(doc_id))
            return False, 'Document doesn`t exist'

        returning_time=self.get_returning_time(returning_time,type_bd,doc_id,user_id)
        free_count = int(self.DBmanager.get_label("free_count", type_bd, doc_id))
        if free_count > 0:

            current_orders = eval(self.DBmanager.get_label("current_docs", "patrons", user_id))
            current_docs_id = []

            for order_id in current_orders:
                order = self.DBmanager.select_label('orders', order_id)
                if order[2] == type_bd:
                    current_docs_id.append(order[3])

            if doc_id in current_docs_id:
                self.log('INFO', 'User {} already have copy of document \'{}\''.format(
                    self.get_user(user_id)['name'], self.get_document(doc_id, type_bd)['title']))
                return False, 'User alredy have copy of document'

            time = date_when_took
            out_of_time = time + timedelta(weeks=returning_time)
            time = str(time)
            out_of_time = str(out_of_time)
            time = time[:time.index(' ')]
            out_of_time = out_of_time[:out_of_time.index(' ')]

            order = {'date': time, 'table': type_bd, "user_id": user_id, "doc_id": doc_id, "active": 0,
                     'out_of_time': out_of_time}

            self.DBmanager.add_order(Packager(order))
            order_id = self.DBmanager.get_max_id('orders')
            history = eval(self.DBmanager.get_label("history", "patrons", user_id))
            current_orders += [order_id]
            history += [order_id]
            free_count -= 1

            self.DBmanager.edit_label(type_bd, ["free_count"], [free_count], doc_id)
            self.DBmanager.edit_label("patrons", ["history", "current_docs"], [str(history), str(current_orders)],
                                      user_id)
            self.log(
                'INFO', 'User {}({}) want to check out document \'{}\' for {} weeks. Returning time is {}'.format(
                    self.get_user(user_id)['name'],
                    self.get_user(user_id)['status'],
                    self.get_document(doc_id, type_bd)['title'],
                    returning_time, out_of_time))
            return True, 'OK'

        else:
            self.log('INFO', 'Not enough copies of document \'{}\''.format(self.get_document(doc_id, type_bd)['title']))
            return False, 'Not enough copies'

    def user_get_doc(self, order_id):
        self.DBmanager.edit_label('orders', ['active'], [1], order_id)

    def return_doc(self, order_id):
        order = self.get_order(order_id)
        user_id, doc_id, doc_type = order["user_id"], order["doc_id"], order["table"]
        curr_doc = eval(self.DBmanager.get_label('current_docs', 'patrons', user_id))
        curr_doc.remove(order['id'])

        free_count = int(self.DBmanager.get_label("free_count", order['table'], doc_id))
        free_count += 1

        self.DBmanager.edit_label(order['table'], ['free_count'], [free_count], doc_id)
        self.DBmanager.edit_label('patrons', ['current_docs'], [str(curr_doc)], user_id)
        self.DBmanager.edit_label('orders', ['active'], [2], order['id'])
        self.log('INFO', 'User {} is returned document {}.'.format(
            self.get_user(user_id)['name'],
            self.get_document(doc_id, order['table'])['title']))
        return True, 'OK'

    def get_user_orders(self, user_id):
        user = self.get_user(user_id)
        if not user:
            return []
        orders_id = eval(user['current_docs'])
        output = []

        for order_id in orders_id:
            order = self.get_order(order_id)
            if order is None:
                continue
            doc = self.DBmanager.select_label(order['table'], order['doc_id'])
            if doc is None:
                continue
            order['doc'] = self.doc_tuple_to_dict(order['table'], doc)
            output.append(order)
        return output
    
    def get_user_history(self, user_id):
        user = self.get_user(user_id)
        if not user:
            return []
        orders_id = eval(user['history'])
        output = []

        for order_id in orders_id:
            order = self.get_order(order_id)
            if order is None:
                continue
            doc = self.DBmanager.select_label(order['table'], order['doc_id'])
            if doc is None:
                continue
            order['doc'] = self.doc_tuple_to_dict(order['table'], doc)
            output.append(order)
        return output

    def get_order(self, order_id):
        order = self.DBmanager.select_label("orders", order_id)
        if order is None:
            self.log('WARNING', 'Can`t find the order for giving id.')
            return None
        return dict(zip(['id', 'time', 'table', 'doc_id', 'user_id', 'time_out', 'active','renewed'], order))

    def get_all_orders(self, by_who_id=-1):
        by_who = 'UNKNOW' if by_who_id == -1 else self.get_user(by_who_id)['name']
        orders = self.DBmanager.select_all('orders')
        self.log('INFO', 'Librarian {} whant to see all orders'.format(by_who))
        return [dict(zip(['id', 'time', 'table', 'doc_id', 'user_id', 'time_out', 'active'], order)) for order in
                orders]

    def get_all_active_orders(self, by_who_id=-1):
        by_who = 'UNKNOW' if by_who_id == -1 else self.get_user(by_who_id)['name']
        orders = self.DBmanager.get_by('active', 'orders', 1)
        self.log('INFO', 'Librarian {} whant to see all active orders'.format(by_who))
        return [dict(zip(['id', 'time', 'table', 'doc_id', 'user_id', 'time_out', 'active'], order)) for order in
                orders]

    def get_all_whaiting_doc(self, by_who_id=-1):
        by_who = 'UNKNOW' if by_who_id == -1 else self.get_user(by_who_id)['name']
        orders = self.DBmanager.get_by('active', 'orders', 0)
        self.log('INFO', 'Librarian {} whant to see all whaiting orders'.format(by_who))
        return [dict(zip(['id', 'time', 'table', 'user_id', 'doc_id', 'active', 'time_out'], order)) for order in
                orders]

    def get_all_returned_orders(self, by_who_id=-1):
        by_who = 'UNKNOW' if by_who_id == -1 else self.get_user(by_who_id)['name']
        orders = self.DBmanager.get_by('active', 'orders', 2)
        self.log('INFO', 'Librarian {} wants to see all returned orders'.format(by_who))
        return [dict(zip(['id', 'time', 'table', 'user_id', 'doc_id', 'active', 'time_out'], order)) for order in
                orders]

    # Method for adding the document in database
    # param: name - Name of the document
    # param: description - about what this document
    # param: author - author of the book
    # param: count - amount of books
    # param: price - price of the book

    def add_document(self, doc, key, by_who_id=0):
        if (doc.keys().__contains__('free_count')):
            doc['free_count'] = doc['count']
        if key == 'book':
            self.DBmanager.add_book(Packager(doc))
        elif key == 'article':
            self.DBmanager.add_article(Packager(doc))
        elif key == 'media':
            self.DBmanager.add_media(Packager(doc))
        elif key == 'reference_book':
            self.DBmanager.add_reference_book(Packager(doc))
        elif key == 'reference_article':
            self.DBmanager.add_reference_article(Packager(doc))

        by_who = 'UNKNOW' if by_who_id == 0 else self.get_user(by_who_id)['name']
        self.log('INFO', '{} \'{}\' is added to system by {}.'.format(key.capitalize(), doc['title'], by_who))

    def modify_document(self, doc, type, by_who_id=0):
        doc_id = doc['id']
        self.DBmanager.edit_label(type, list(doc.keys()), list(doc.values()), doc_id)
        by_who = 'UNKNOW' if by_who_id == 0 else self.get_user(by_who_id)['name']
        log = 'Document with id {} was modified by {}: '.format(
            doc_id, by_who) + ', '.join(['new ' + str(key) + ' is ' + str(doc[key]) for key in doc.keys()])
        self.log('INFO', log)

    def add_copies_of_document(self, doc_type, doc_id, new_count, by_who_id=0):
        doc = self.get_document(doc_id, doc_type)

        new_free_count = doc['free_count'] + new_count  # - doc['count']
        self.modify_document({'id': doc_id, 'count': doc['count'] + new_count, 'free_count': new_free_count}, doc_type,
                             by_who_id)

    def delete_document(self, doc_id, doc_type):
        self.DBmanager.delete_label(doc_type, doc_id)
        self.log('INFO', 'Document {} was deleted'.format(doc_id))

    def doc_tuple_to_dict(self, type, doc_tuple):
        if type == 'book':
            return dict(
                zip(['id', 'title', 'authors', 'description', 'count', 'free_count', 'price', 'best_seller',
                     'keywords', 'queue'],
                    list(doc_tuple)))
        elif type == 'article':
            return dict(zip(
                ['id', 'title', 'authors', 'journal', 'count', 'free_count', 'price', 'keywords', 'issue', 'editors',
                 'date', 'queue'], list(doc_tuple)))
        elif type == 'media':
            return dict(
                zip(['id', 'title', 'authors', 'count', 'free_count', 'price', 'keywords', 'queue'], list(doc_tuple)))
        elif type == 'reference_book':
            return dict(
                zip(['id', 'title', 'authors', 'keywords'], list(doc_tuple)))

        elif type == 'reference_article':
            return dict(zip(
                ['id', 'title', 'authors', 'journal', 'keywords', 'issue', 'editors',
                 'date'], list(doc_tuple)))

    def get_document(self, doc_id, type_bd):
        return self.doc_tuple_to_dict(type_bd, self.DBmanager.select_label(type_bd, doc_id))

    def get_all_reference_book(self):
        rows = self.DBmanager.select_all("reference_book")
        return [dict(
            zip(['id', 'title', 'authors', 'description', 'keywords'],
                list(book))) for book in rows]

    def get_all_reference_articles(self):
        rows = self.DBmanager.select_all("reference_article")
        return [dict(zip(
            ['id', 'title', 'authors', 'journal' 'keywords', 'issue', 'editors',
             'date'], list(article))) for article in rows]

    # Return all books from database
    def get_all_books(self):
        rows = self.DBmanager.select_all("book")
        return [dict(
            zip(['id', 'title', 'authors', 'description', 'count', 'free_count', 'price', 'best_seller', 'keywords',
                 'queue'],
                list(book))) for book in rows]

    # Return all articles from database
    def get_all_articles(self):
        rows = self.DBmanager.select_all("article")
        return [dict(zip(
            ['id', 'title', 'authors', 'journal', 'count', 'free_count', 'price', 'keywords', 'issue', 'editors',
             'date', 'queue'], list(article))) for article in rows]

    # Return all media from database
    def get_all_media(self):
        rows = self.DBmanager.select_all("media")
        return [dict(zip(['id', 'title', 'authors', 'count', 'free_count', 'price', 'keywords', 'queue'], list(media)))
                for media in rows]

    def get_all_doctype(self, doc_type, by_who_id=-1):
        by_who = 'UNKNOW' if by_who_id == -1 else self.get_user(by_who_id)['name']
        if doc_type == 'book':
            return self.get_all_books()
        elif doc_type == 'article':
            return self.get_all_articles()
        elif doc_type == 'media':
            return self.get_all_media()
        self.log('INFO', 'Get all {} by {}.'.format(doc_type.capitalize(), by_who))

    def get_documents_by_title(self, title, type_db, by_who_id=-1):
        by_who = 'UNKNOW' if by_who_id == -1 else self.get_user(by_who_id)['name']
        documents = self.DBmanager.get_by('title', type_db, title)
        self.log('INFO', 'Get {} by title {} by {}.'.format(type_db.capitalize(), title, by_who))
        return [self.doc_tuple_to_dict(type_db, i) for i in documents]

    def get_documents_by_authors(self, authors, type_db, by_who_id=-1):
        by_who = 'UNKNOW' if by_who_id == -1 else self.get_user(by_who_id)['name']
        documents = self.get_all_doctype(type_db)
        output = []
        for doc in documents:
            if all([author in doc['authors'].split(';') for author in authors]):
                output.append(doc)
        self.log('INFO', 'Get {} by authors: {}.'.format(type_db.capitalize(), ', '.join(authors)))
        return output
