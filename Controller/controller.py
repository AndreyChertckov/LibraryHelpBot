import logging
from datetime import datetime, timedelta, date
from Bot.func_data import tuple_to_dict
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
            formater = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
        self.outstanding = []

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
        self.log('INFO', 'User {} signed up. Waiting for librarians confirmation.'.format(
            user_info['name']))

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
        by_who = 'UNKNOW' if librarian_id == - \
            1 else self.get_user(librarian_id)['name']
        self.log('INFO', 'User status {} is confirmed by {}.'.format(
            user['name'], by_who))
        return True

    # Move patron from table patrons to table librarians
    # param: user_id : id of user
    def upto_librarian(self, user_id):
        user_info = self.get_user(user_id)
        user_info.pop('current_docs', 0)
        user_info.pop('history', 0)
        self.delete_user(user_id)
        self.DBmanager.add_librarian(Packager(user_info))
        self.log('INFO', 'User {} is upgraded to librarian'.format(
            user_info['name']))

    def modify_user(self, new_user_info, by_who_id=0):
        user_id = new_user_info['id']
        self.DBmanager.edit_label('patrons', list(
            new_user_info.keys()), list(new_user_info.values()), user_id)
        by_who = 'UNKNOW' if by_who_id == 0 else self.get_user(by_who_id)[
            'name']
        log = 'User with id {} was modified by {}: '.format(
            user_id, by_who) + ', '.join(
            ['new ' + str(key) + ' is ' + str(new_user_info[key]) for key in new_user_info.keys()])
        self.log('INFO', log)

    # Delete user by user_id
    # param: user_id: id of user
    def delete_user(self, user_id, librarian_id = -1):
        table = ['unauthorized', 'unconfirmed', 'patrons',
                 'librarians'][self.user_type(user_id)]
        if table != 'unauthorized':
            user = self.get_user(user_id)
            if table == 'patrons' and user['current_docs'] != '[]':
                return False
            for order_id in user['history']:
                self.DBmanager.delete_label('orders',order_id)
            self.DBmanager.delete_label(table, user_id)
            by_who = 'UNKNOW' if librarian_id == -1 else self.get_user(librarian_id)['name']
            log = 'User {} is deleted by {}.'.format(user_id, by_who)
            self.log('INFO', log)
            return True

    # Return all users who don`t confirmed
    def get_all_unconfirmed(self):
        return [tuple_to_dict('unconfirmed', user) for user in self.DBmanager.select_all("unconfirmed")]

    # Return all patrons from database
    def get_all_patrons(self):
        rows = self.DBmanager.select_all("patrons")
        return [tuple_to_dict('patrons', user) for user in rows]

    # Return all librarians from database
    def get_all_librarians(self):
        rows = self.DBmanager.select_all("librarians")
        return [tuple_to_dict('librarians', user) for user in rows]

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
    # or false if user does not exist
    def get_user(self, user_id, status=None):
        types = {0: "unauthorized", 1: 'unconfirmed',
                 2: 'patrons', 3: 'librarians'}
        if not status:
            status = self.user_type(user_id)
        user_type = types[status]
        if status:
            return tuple_to_dict(user_type, self.DBmanager.select_label(user_type, user_id))
        else:
            self.log('WARNING', 'User with id {} not found.'.format(user_id))
            return False

    # Returns in which table the user is located
    # param : user_id - id of user
    # return : if 0 then user is unauthorized
    #          if 1 then user is unconfirmed
    #          if 2 then user is patron
    #          if 3 then user is admin
    def user_type(self, user_id):
        types = {"unauthorized": 0, 'unconfirmed': 1, 'patron': 2, 'admin': 3}
        if self.DBmanager.select_label('librarians', user_id):
            return types['admin']
        elif self.DBmanager.select_label('patrons', user_id):
            return types['patron']
        elif self.DBmanager.select_label('unconfirmed', user_id):
            return types['unconfirmed']
        else:
            return types['unauthorized']

    def add_queue_order(self, user_id, doc_type, doc_id):
        priority_dict = {'Student': 0, 'Instructor': 1,
                         'TA': 2, 'Visiting Professor': 3, 'Professor': 4}
        status = self.DBmanager.get_label('status', 'patrons', user_id)
        mas = eval(self.DBmanager.get_label('queue', doc_type, doc_id))
        priority = priority_dict[status]
        if mas[priority].__contains__(user_id):
            return False, "You are already in queue"
        current = eval(self.DBmanager.get_label(
            'current_docs', 'patrons', user_id))

        for i in current:
            order = self.get_order(i)
            if order['doc_id'] == doc_id:
                return False, "You already have this document"

        mas[priority] += [user_id]
        self.DBmanager.edit_label(doc_type, ['queue'], [str(mas)], doc_id)
        queue = eval(self.DBmanager.get_label('queue', 'patrons', user_id))
        queue += [(doc_id, doc_type)]
        self.DBmanager.edit_label('patrons', ['queue'], [str(queue)], user_id)
        return True, "User was added in queue"

    def get_user_queue(self, user_id):
        queue = eval(self.DBmanager.get_label('queue', 'patrons', user_id))
        return queue

    def delete_user_queue(self, user_id, type_of_doc, doc_id):
        priority_dict = {'Student': 0, 'Instructor': 1,
                         'TA': 2, 'Visiting Professor': 3, 'Professor': 4}
        queue = eval(self.DBmanager.get_label('queue', 'patrons', user_id))
        for i in queue:
            if (i == (doc_id, type_of_doc)):
                queue.remove(i)
        doc_queue = eval(self.DBmanager.get_label(
            'queue', type_of_doc, doc_id))
        priority = priority_dict[self.get_user(user_id)['status']]
        doc_queue[priority].remove(user_id)
        self.DBmanager.edit_label(type_of_doc, ['queue'], [
                                  str(doc_queue)], doc_id)
        self.DBmanager.edit_label('patrons', ['queue'], [str(queue)], user_id)

    def renew_item(self, order_id, cur_date=datetime.now()):

        order = self.get_order(order_id)
        if (order['doc_id'], order['table']) in self.outstanding:
            return False

        user = self.get_user(order['user_id'])
        new_date = (datetime.strptime(
            order['time_out'], '%Y-%m-%d') + timedelta(weeks=1)).date().isoformat()
        if order['renewed'] == 0:
            self.DBmanager.edit_label('orders', ['out_of_time', 'renewed'], [
                                      new_date, 1], order_id)
            return True
        elif user['status'] == 'Visiting Professor':
            self.DBmanager.edit_label(
                'orders', ['out_of_time'], [new_date], order_id)
            return True
        return False

    def delete_doc_queue(self, doc_id, doc_type):
        queue = eval(self.DBmanager.get_label('queue', doc_type, doc_id))

        for i in queue:
            for id in i:
                self.delete_user_queue(id, doc_type, doc_id)

    def get_document_queue(self, doc_type, doc_id):
        output = []
        queue = eval(self.DBmanager.get_label('queue', doc_type, doc_id))
        for i in range(1, 5):
            queue[0].extend(queue[i])
        queue = queue[0]
        for user_id in queue:
            output.append(self.get_user(user_id))
        return output

    # def delete_queue_order(self, user_id, type_of_doc, doc_id):

    def get_user_by_name(self, name):
        user = self.DBmanager.get_by('name', 'patrons', name)[0]
        return tuple_to_dict('patrons', user)

    def get_returning_time(self, returning_time, type_bd, doc_id, user_id):
        user_status = self.DBmanager.get_label('status', 'patrons', user_id)
        if returning_time == 0 and type_bd == 'book':
            is_best_seller = self.DBmanager.get_label(
                'best_seller', type_bd, doc_id) == 1
            returning_time = 3 if user_status == 'Student' else 4
            returning_time = 2 if is_best_seller else returning_time
            returning_time = 4 if user_status == 'Professor' else returning_time
        elif type_bd != 'book':
            returning_time = 2
        returning_time = 1 if user_status == 'Visiting Professor' else returning_time
        return returning_time

    def check_out_doc(self, user_id, doc_id, type_bd='book', returning_time=0, date_when_took=datetime.now()):
        if self.DBmanager.select_label(type_bd, doc_id) is None:
            self.log('WARNING', 'Document with id {} not found.'.format(doc_id))
            return False, 'Document doesn`t exist'

        returning_time = self.get_returning_time(
            returning_time, type_bd, doc_id, user_id)
        free_count = int(self.DBmanager.get_label(
            "free_count", type_bd, doc_id))
        if free_count > 0:

            current_orders = eval(self.DBmanager.get_label(
                "current_docs", "patrons", user_id))
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
                     'out_of_time': out_of_time, 'renewed': 0}

            self.DBmanager.add_order(Packager(order))
            order_id = self.DBmanager.get_max_id('orders')
            history = eval(self.DBmanager.get_label(
                "history", "patrons", user_id))
            current_orders += [order_id]
            history += [order_id]
            free_count -= 1

            self.DBmanager.edit_label(
                type_bd, ["free_count"], [free_count], doc_id)
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
            self.log('INFO', 'Not enough copies of document \'{}\''.format(
                self.get_document(doc_id, type_bd)['title']))
            return False, 'Not enough copies'

    def user_get_doc(self, order_id):
        self.DBmanager.edit_label('orders', ['active'], [1], order_id)

    def calculate_fine(self, order, cur_date=date.today()):
        order['doc'] = self.get_document(order['doc_id'], order['table'])
        time_out = datetime.strptime(order['time_out'], "%Y-%m-%d").date()
        fine = (cur_date - time_out).days * 100
        return max(min(fine, order['doc']['price']), 0)

    # Need to pass tests
    def get_overdue(self, user_id, date_=date.today()):
        user_orders = self.get_user_orders(user_id)
        overdue = []
        for id in user_orders:
            time_out = datetime.strptime(id['time_out'], "%Y-%m-%d").date()
            overdue.append((self.DBmanager.get_label('title', id['table'], id['doc_id']),
                            (date_ - time_out).days))
        return overdue

    def get_fine(self, user_id, date):
        user_orders = self.get_user_orders(user_id)
        fine = []
        for id in user_orders:
            fine.append((self.DBmanager.get_label('title', id['table'], id['doc_id']),
                         self.calculate_fine(id, date)))
        return fine

    def get_user_due(self, user_id):
        user_orders = self.get_user_orders(user_id)
        doc = []
        for order in user_orders:
            doc.append((self.DBmanager.get_label('title', order['table'], order['doc_id']),
                        order['time_out']))
        return doc

    def outstanding_request(self, doc_id, doc_type, date=date.today()):
        orders = self.get_all_orders()
        self.outstanding.append((doc_id, doc_type))
        deleted_from_waiting_list = [i['id']
                                     for i in self.get_document_queue(doc_type, doc_id)]
        self.delete_doc_queue(doc_id, doc_type)
        notified_patrons = []
        for order in orders:
            if order['table'] == doc_type and str(order['doc_id']) == str(doc_id) and order['active'] == 1:
                self.DBmanager.edit_label('orders', ['out_of_time'], [
                                          str(date)], order['id'])
                notified_patrons.append(order['user_id'])
        return [deleted_from_waiting_list, notified_patrons]

    def return_doc(self, order_id, testing=False):
        order = self.get_order(order_id)
        fine = self.calculate_fine(order)
        user_id, doc_id, doc_type = order["user_id"], order["doc_id"], order["table"]
        curr_doc = eval(self.DBmanager.get_label(
            'current_docs', 'patrons', user_id))
        curr_doc.remove(order['id'])
        if (doc_id, doc_type) in self.outstanding:
            self.outstanding.remove((doc_id, doc_type))

        free_count = int(self.DBmanager.get_label(
            "free_count", order['table'], doc_id))
        free_count += 1

        returned_time = str(datetime.now()).split(' ')[0]

        self.DBmanager.edit_label(
            order['table'], ['free_count'], [free_count], doc_id)
        self.DBmanager.edit_label('patrons', ['current_docs'], [
                                  str(curr_doc)], user_id)
        self.DBmanager.edit_label('orders', ['active', 'out_of_time'], [
                                  2, returned_time], order['id'])
        self.log('INFO', 'User {} is returned document {}.'.format(
            self.get_user(user_id)['name'],
            self.get_document(doc_id, order['table'])['title']))
        queue = self.get_document_queue(order["table"], doc_id)
        next_owner = 0
        queue_was_used = [False]
        if len(queue) != 0:

            next_owner = queue[0]
            if (not testing):
                self.delete_user_queue(
                    next_owner['id'], order["table"], doc_id)
                self.check_out_doc(next_owner['id'], doc_id, order["table"])
            queue_was_used = [True, next_owner]
        return True, fine, queue_was_used, next_owner['id']

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
            order['doc'] = tuple_to_dict(order['table'], doc)
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
            order['doc'] = tuple_to_dict(order['table'], doc)
            output.append(order)
        return output
    
    def delete_waiting_order(self,order_id):
        order = self.get_order(order_id)
        user_id, doc_id = order["user_id"], order["doc_id"]
        curr_doc = eval(self.DBmanager.get_label(
            'current_docs', 'patrons', user_id))
        curr_doc.remove(order['id'])
        free_count = int(self.DBmanager.get_label(
            "free_count", order['table'], doc_id))
        free_count += 1
        self.DBmanager.edit_label(
            order['table'], ['free_count'], [free_count], doc_id)
        self.DBmanager.edit_label('patrons', ['current_docs'], [
                                  str(curr_doc)], user_id)
        self.DBmanager.delete_label('orders',order_id)
        
    def get_order(self, order_id):
        order = self.DBmanager.select_label("orders", order_id)
        if order is None:
            self.log('WARNING', 'Can`t find the order for giving id.')
            return None
        return tuple_to_dict('order', order)

    def get_all_orders(self):
        orders = self.DBmanager.select_all('orders')
        output = [tuple_to_dict('order', order) for order in orders]
        for order in output:
            doc = self.DBmanager.select_label(order['table'], order['doc_id'])
            order['doc'] = tuple_to_dict(order['table'], doc)
            order['user'] = self.get_user(order['user_id'])
        return output

    def get_all_active_orders(self):
        orders = self.DBmanager.get_by('active', 'orders', 1)
        output = [tuple_to_dict('order', order) for order in orders]
        for order in output:
            doc = self.DBmanager.select_label(order['table'], order['doc_id'])
            order['doc'] = tuple_to_dict(order['table'], doc)
            order['user'] = self.get_user(order['user_id'])
        return output

    def get_all_waiting_doc(self):
        orders = self.DBmanager.get_by('active', 'orders', 0)
        output = [tuple_to_dict('order', order) for order in orders]
        for order in output:
            doc = self.DBmanager.select_label(order['table'], order['doc_id'])
            order['doc'] = tuple_to_dict(order['table'], doc)
            order['user'] = self.get_user(order['user_id'])
        return output

    def get_all_returned_orders(self):
        orders = self.DBmanager.get_by('active', 'orders', 2)
        output = [tuple_to_dict('order', order) for order in orders]
        for order in output:
            doc = self.DBmanager.select_label(order['table'], order['doc_id'])
            order['doc'] = tuple_to_dict(order['table'], doc)
            order['user'] = self.get_user(order['user_id'])
        return output

    # Method for adding the document in database
    # param: name - Name of the document
    # param: description - about what this document
    # param: author - author of the book
    # param: count - amount of books
    # param: price - price of the book

    def add_document(self, doc, key, by_who_id=0):
        if doc.keys().__contains__('free_count'):
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

        by_who = 'UNKNOW' if by_who_id == 0 else self.get_user(by_who_id)[
            'name']
        self.log('INFO', '{} \'{}\' is added to system by {}.'.format(
            key.capitalize(), doc['title'], by_who))

    def modify_document(self, doc, doc_type, by_who_id=0):
        doc_id = doc['id']
        self.DBmanager.edit_label(doc_type, list(
            doc.keys()), list(doc.values()), doc_id)
        by_who = 'UNKNOW' if by_who_id == 0 else self.get_user(by_who_id)[
            'name']
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

    def get_document(self, doc_id, type_bd):
        return tuple_to_dict(type_bd, self.DBmanager.select_label(type_bd, doc_id))

    def get_all_reference_book(self):
        rows = self.DBmanager.select_all("reference_book")
        return [tuple_to_dict('reference_book', book) for book in rows]

    def get_all_reference_articles(self):
        rows = self.DBmanager.select_all("reference_article")
        return [tuple_to_dict('reference_article', article) for article in rows]

    # Return all books from database
    def get_all_books(self):
        return [tuple_to_dict('book', book) for book in self.DBmanager.select_all("book")]

    # Return all articles from database
    def get_all_articles(self):
        return [tuple_to_dict('article', article) for article in self.DBmanager.select_all("article")]

    # Return all media from database
    def get_all_media(self):
        rows = self.DBmanager.select_all("media")
        return [tuple_to_dict('media', media) for media in rows]

    def get_all_doctype(self, doc_type, by_who_id=-1):
        if doc_type == 'book':
            return self.get_all_books()
        elif doc_type == 'article':
            return self.get_all_articles()
        elif doc_type == 'media':
            return self.get_all_media()

    def get_documents_by_title(self, title, type_db, by_who_id=-1):
        documents = self.DBmanager.get_by('title', type_db, title)
        return [tuple_to_dict(type_db, i) for i in documents]

    def get_documents_by_authors(self, authors, type_db, by_who_id=-1):
        documents = self.get_all_doctype(type_db)
        output = []
        for doc in documents:
            if all([author in doc['authors'].split(';') for author in authors]):
                output.append(doc)
        return output
