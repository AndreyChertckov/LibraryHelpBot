from flask import Blueprint, request, redirect, jsonify
from Bot.func_data import keyboard_dict, tuple_to_dict
from telegram import ReplyKeyboardMarkup as RKM
import logging

from AdminSite.utils import generate_sault, md5_hash, create_session, check_session, check_privilege

from configs import host, port, inet_addr, telegram_alias

logger = logging.getLogger('api-site')


def security_decorator_maker(privilege_val):
    def security_decorator(api_method):
        def decorator(self):
            if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'), self.dbmanager):
                if check_privilege(request.cookies.get('session_id'), privilege_val, self.dbmanager):
                    return api_method(self)
                else:
                    return 'Access forbidden.'
            else:
                return 'Sign in before.'

        return decorator

    return security_decorator


def notification_decorator_maker(message, reply_markup=None):
    def notification_decorator(method):
        def decorator(self):
            if self.is_have_notification:
                result = method(self)
                for chat_id in self.notification_id:
                    self.notification.send_message(chat_id, message, reply_markup)
                self.notification_id = []
                return result
            else:
                return method(self)
        return decorator

    return notification_decorator


class API:
    def __init__(self, app, controller, dbmanager, notification):
        self.blueprint = Blueprint('api', __name__)
        self.init_handlers()
        self.app = app
        self.dbmanager = dbmanager
        self.app.register_blueprint(self.blueprint)
        self.controller = controller
        self.notification = notification
        self.is_have_notification = notification is not None
        self.notification_id = []

    def init_handlers(self):
        add_rule = self.blueprint.add_url_rule
        add_rule('/signin', 'signin', self.signin_post, methods=['POST'])
        add_rule('/signup', 'signup', self.signup_post, methods=['POST'])
        add_rule('/signout', 'signout', self.signout_get, methods=['GET'])
        add_rule('/api/get_account_info', 'get_account_info', self.get_account_info, methods=['POST'])
        add_rule('/api/get_verification_links', 'get_verification_links', self.get_verification_links, methods=['POST'])
        add_rule('/api/generate_invite_link', 'generate_invite_link', self.generate_verification_string, methods=['POST'])
        add_rule('/api/get_telegram_verification_message', 'get_telegram_verification_message', self.get_verification_message_post, methods=['POST'])
        add_rule('/api/get_all_unconfirmed', 'get_all_unconfirmed', self.get_all_unconfirmed_post, methods=['POST'])
        add_rule('/api/confirm_user', 'confirm_user', self.confirm_user_post, methods=['POST'])
        add_rule('/api/modify_user', 'modify_user', self.modify_user_post, methods=['POST'])
        add_rule('/api/delete_user', 'delete_user', self.delete_user_post, methods=['POST'])
        add_rule('/api/get_all_patrons', 'get_all_patrons', self.get_all_patrons_post, methods=['POST'])
        add_rule('/api/get_all_librarians', 'get_all_librarians', self.get_all_librarians_post, methods=['POST'])
        add_rule('/api/get_librarian_by_name', 'get_librarian_by_name', self.get_librarian_by_name_post, methods=['POST'])
        add_rule('/api/get_user', 'get_user', self.get_user_post, methods=['POST'])
        add_rule('/api/get_user_by_name', 'get_user_by_name', self.get_user_by_name_post, methods=['POST'])
        add_rule('/api/reject_order', 'reject_order', self.reject_order_post, methods=['POST'])
        add_rule('/api/user_get_doc', 'user_get_doc', self.user_get_doc_post, methods=['POST'])
        add_rule('/api/return_doc', 'return_doc', self.return_doc_post, methods=['POST'])
        add_rule('/api/get_user_orders', 'get_user_orders', self.get_user_orders_post, methods=['POST'])
        add_rule('/api/get_user_history', 'get_user_history', self.get_user_history_post, methods=['POST'])
        add_rule('/api/get_order', 'get_order', self.get_order_post, methods=['POST'])
        add_rule('/api/get_all_orders', 'get_all_orders', self.get_all_orders_post, methods=['POST'])
        add_rule('/api/get_all_active_orders', 'get_all_active_orders', self.get_all_active_orders_post, methods=['POST'])
        add_rule('/api/get_all_waiting_doc', 'get_all_waiting_doc', self.get_all_waiting_doc_post, methods=['POST'])
        add_rule('/api/get_all_returned_doc', 'get_all_returned_doc', self.get_all_returned_doc, methods=['POST'])
        add_rule('/api/add_document', 'add_document', self.add_document_post, methods=['POST'])
        add_rule('/api/modify_document', 'modify_document', self.modify_docment_post, methods=['POST'])
        add_rule('/api/add_copies_of_doc', 'add_copies_of_doc', self.add_copies_of_doc_post, methods=['POST'])
        add_rule('/api/delete_document', 'delete_document', self.delete_document_post, methods=['POST'])
        add_rule('/api/get_document', 'get_document', self.get_document_post, methods=['POST'])
        add_rule('/api/get_all_doctype', 'get_all_doctype', self.get_all_doctype_post, methods=['POST'])
        add_rule('/api/get_documents_by_title', 'get_documents_by_title', self.get_documents_by_title_post, methods=['POST'])
        add_rule('/api/get_documents_by_authors', 'get_documents_by_authors', self.get_documents_by_authors_post, methods=['POST'])
        add_rule('/api/get_queue_on_document', 'get_queue_on_document', self.get_queue_on_documnent_post, methods=['POST'])
        add_rule('/api/outstanding', 'outstanding', self.outstanding_post, methods=['POST'])

    def signin_post(self):
        login = request.values.get('login')
        passwd = md5_hash(request.values.get('password').encode('utf-8'))
        if self.dbmanager.get_user(login, passwd) is None:
            response = self.app.make_response(redirect('/signin'))
            response.set_cookie('error', 'Login error')
            return response
        response = self.app.make_response(redirect('/'))
        response.set_cookie('session_id', create_session(login, passwd, self.dbmanager))
        return response

    @security_decorator_maker(3)
    def generate_verification_string(self):
        if 'privilege' in request.values:
            string = md5_hash(generate_sault())
            self.dbmanager.insert_verification_string(string, request.values.get('privilege'))
            return string
        else:
            return 'Need privilege value'

    @security_decorator_maker(3)
    def get_verification_links(self):
        if int(port) == 80:
            link = 'http://{}/signup?verification_string='.format(inet_addr)
        elif int(port) == 443:
            link = 'https://{}/signup?verification_string='.format(inet_addr)
        else:
            link = 'http://{}:{}/signup?verification_string='.format(inet_addr, port)
        ver_strings = self.dbmanager.all_verification_strings(1)
        pattern = '<a href="#">%s{}</a> -------- Privilege level: {}' % link
        if ver_strings:
            output = [pattern.format(string[0], self.dbmanager.get_privilege_by_verification_string(string[0])[0] + 1) for string in ver_strings]
            return jsonify(output)
        else:
            return jsonify([])

    @security_decorator_maker(0)
    def get_verification_message_post(self):
        session_id = request.cookies.get('session_id')
        user_id = self.dbmanager.get_user_id_by_session(session_id)
        ver_val = self.dbmanager.get_verification_string(user_id)
        pattern = 'Write to telegram bot(<a href="https://t.me/{}">https://t.me/{}</a>) this line</br> /verification {}'
        return pattern.format(telegram_alias, telegram_alias, ver_val[0])

    def signup_post(self):
        values = request.values
        ver_str = 'verification_string'
        if ver_str in values and self.dbmanager.if_verification_string_exist(values.get(ver_str), 1):
            keys = ['login', 'name', 'phone', 'address']
            user = dict(zip(keys, [values.get(key) for key in keys]))
            user['passwd'] = md5_hash(values.get('password').encode('utf-8'))
            user['privilege'] = self.dbmanager.get_privilege_by_verification_string(values.get(ver_str))
            self.dbmanager.create_user(user)
            response = self.app.make_response(redirect('/'))
            session_id = create_session(user['login'], user['passwd'], self.dbmanager)
            response.set_cookie('session_id', session_id)
            user_id = self.dbmanager.get_user_id_by_session(session_id)
            self.dbmanager.activate_verification_string(values.get(ver_str), user_id)
            return response
        else:
            return 'Please write to another librarian to get signup link.'

    def signout_get(self):
        session_id = request.cookies['session_id']
        self.dbmanager.delete_session(session_id)
        response = self.app.make_response(redirect('/'))
        response.set_cookie('session_id', '', expires=0)
        return response

    def get_account_info(self):
        session_id = request.cookies['session_id']
        user_id = self.dbmanager.get_user_id_by_session(session_id)[0]
        user = tuple_to_dict('account', self.dbmanager.get_user_by_id(user_id))
        user.pop('passwd', 0)
        user.pop('chat_id', 0)
        return jsonify(user)

    @security_decorator_maker(0)
    def get_all_unconfirmed_post(self):
        return jsonify(self.controller.get_all_unconfirmed())

    @security_decorator_maker(1)
    @notification_decorator_maker("Your application was confirmed", RKM(keyboard_dict["auth"], True))
    def confirm_user_post(self):
        if 'user_id' in request.values:
            user_id = request.values.get('user_id')
            librarian_id = self.dbmanager.get_user_id_by_session(request.cookies.get('session_id'))[0]
            success = self.controller.confirm_user(user_id,librarian_id)
            if success:
                self.notification_id = [user_id]
            return 'OK' if success else "Something went wrong"
        else:
            return 'Need id of user'

    @security_decorator_maker(0)
    @notification_decorator_maker("You information was updated")
    def modify_user_post(self):
        keys = ['id', 'name', 'phone', 'address', 'status']
        user = {key: request.values.get(key) for key in keys if key in request.values}
        if not ('id' in user):
            return 'Need id'
        librarian_id = self.dbmanager.get_user_id_by_session(request.cookies.get('session_id'))[0]
        self.controller.modify_user(user,librarian_id)
        self.notification_id = [user['id']]
        return 'OK'

    @security_decorator_maker(2)
    @notification_decorator_maker("Your account was deleted", RKM(keyboard_dict["unauth"], True))
    def delete_user_post(self):
        if 'user_id' in request.values:
            self.notification_id = [request.values.get('user_id')]
            return str(self.controller.delete_user(request.values.get('user_id')))
        else:
            return 'Need id of user'

    @security_decorator_maker(0)
    def get_all_patrons_post(self):
        return jsonify(self.controller.get_all_patrons())

    @security_decorator_maker(0)
    def get_all_librarians_post(self):
        librarians_list = [dict(zip(['id', 'name', 'phone', 'address', 'privilege'], tup))
                           for tup in self.dbmanager.get_users()]

        return jsonify(librarians_list)

    @security_decorator_maker(0)
    def get_librarian_by_name_post(self):
        librarians_list = tuple_to_dict('librarians', self.dbmanager.get_user_by_name(request.values.get('name')))
        return jsonify(librarians_list)

    @security_decorator_maker(0)
    def get_user_post(self):
        if 'user_id' in request.values:
            return jsonify(self.controller.get_user(request.values.get('user_id')))
        else:
            return 'Need id of user'

    @security_decorator_maker(0)
    def get_user_by_name_post(self):
        if 'name' in request.values:
            return jsonify(self.controller.get_user_by_name(request.values.get('name')))
        else:
            return 'Need id of user'

    @security_decorator_maker(0)
    def reject_order_post(self):
        if 'order_id' in request.values:
            self.controller.delete_waiting_order(request.values.get('order_id'))
            return 'OK'
        else:
            return 'Need id of order'

    @security_decorator_maker(0)
    def user_get_doc_post(self):
        if 'order_id' in request.values:
            self.controller.user_get_doc(request.values.get('order_id'))
            return 'OK'
        else:
            return 'Need id of order'

    @security_decorator_maker(0)
    @notification_decorator_maker('You returned document')
    def return_doc_post(self):
        if 'order_id' in request.values:
            *_, self.notification_id = self.controller.return_doc(request.values.get('order_id'))
        else:
            return 'Need id of order'

    @security_decorator_maker(0)
    def get_user_orders_post(self):
        if 'user_id' in request.values:
            return jsonify(self.controller.get_user_orders(request.values.get('user_id')))
        else:
            return 'Need id of user'

    @security_decorator_maker(0)
    def get_user_history_post(self):
        if 'user_id' in request.values:
            return jsonify(self.controller.get_user_history(request.values.get('user_id')))
        else:
            return 'Need id of user'

    @security_decorator_maker(0)
    def get_order_post(self):
        if 'order_id' in request.values:
            return jsonify(self.controller.get_order(request.values.get('order_id')))
        else:
            return 'Need id of order'

    @security_decorator_maker(0)
    def get_all_orders_post(self):
        return jsonify(self.controller.get_all_orders())

    @security_decorator_maker(0)
    def get_all_active_orders_post(self):
        return jsonify(self.controller.get_all_active_orders())

    @security_decorator_maker(0)
    def get_all_waiting_doc_post(self):
        return jsonify(self.controller.get_all_waiting_doc())

    @security_decorator_maker(0)
    def get_all_returned_doc(self):
        return jsonify(self.controller.get_all_returned_orders())

    @security_decorator_maker(1)
    def add_document_post(self):
        values = request.values
        keys = ['title', 'description', 'authors', 'count',
                'price', 'keywords', 'best_seller', 'free_count']
        doc_type = values.get('type')
        if doc_type == 'article':
            keys.extend(['journal', 'issue', 'editors', 'date'])
        if all([key in values for key in keys]):
            document = dict(zip(keys, [values.get(key) for key in keys]))
            document['best_seller'] = int(document['best_seller'])
            librarian_id = self.dbmanager.get_user_id_by_session(request.cookies.get('session'))[0]
            self.controller.add_document(document, doc_type,librarian_id)
            return 'OK'
        else:
            print([key for key in values.keys()])
            return 'Not enough keys'

    @security_decorator_maker(0)
    def modify_docment_post(self):
        values = request.values
        keys = ['id', 'title', 'authors', 'description', 'price',
                'best_seller', 'keywords', 'journal', 'issue', 'editors', 'date']
        doc = {key: values.get(key) for key in keys if key in values}
        if not ('id' in doc):
            return 'Need id'
        if not ('type' in values):
            return 'Need type'
        librarian_id = self.dbmanager.get_user_id_by_session(request.cookies.get('session'))[0]
        self.controller.modify_document(doc, values.get('type'),librarian_id)
        return 'OK'

    @security_decorator_maker(0)
    @notification_decorator_maker("You can get the document")
    def add_copies_of_doc_post(self):
        values = request.values
        if not ('id' in values):
            return 'Need id'
        if not ('delta_count' in values):
            return 'Need delta count'
        if not ('type' in values):
            return 'Need type'
        queue = self.controller.get_document_queue(values.get('type'),values.get('id'))
        if int(values.get('delta_count')) > 0:
            for i in range(min([len(queue),int(values.get('delta_count'))])):
                self.notification_id.append(queue[i]['id'])
                self.controller.delete_user_queue(queue[i]['id'],values.get('type'),values.get('id'))
        self.controller.add_copies_of_document(values.get('type'), values.get('id'), int(values.get('delta_count')))
        return 'OK'

    @security_decorator_maker(2)
    def delete_document_post(self):
        values = request.values
        if not ('id' in values):
            return 'Need id'
        if not ('type' in values):
            return 'Need type'
        self.controller.delete_document(values.get('id'), values.get('type'))
        return 'OK'

    @security_decorator_maker(0)
    def get_document_post(self):
        values = request.values
        if not ('id' in values):
            return 'Need id'
        if not ('type' in values):
            return 'Need type'
        return jsonify(self.controller.get_document(values.get('id'), values.get('type')))

    @security_decorator_maker(0)
    def get_all_doctype_post(self):
        if not ('type' in request.values):
            return 'Need type'
        return jsonify(self.controller.get_all_doctype(request.values.get('type')))

    @security_decorator_maker(0)
    def get_documents_by_title_post(self):
        values = request.values
        if not ('title' in values):
            return 'Need title'
        if not ('type' in values):
            return 'Need type'
        return jsonify(self.controller.get_documents_by_title(values.get('title'), values.get('type')))

    @security_decorator_maker(0)
    def get_documents_by_authors_post(self):
        values = request.values
        if not ('authors' in values):
            return 'Need authors'
        if not ('type' in values):
            return 'Need type'
        return jsonify(self.controller.get_documents_by_title(values.get('authors'), values.get('type')))

    @security_decorator_maker(0)
    def get_queue_on_documnent_post(self):
        values = request.values
        if not ('doc_id' in values):
            return 'Need id'
        if not ('type' in values):
            return 'Need type'
        return jsonify(self.controller.get_document_queue(values.get('type'), values.get('doc_id')))

    @security_decorator_maker(1)
    @notification_decorator_maker("You are removed from queue.")
    def outstanding_post(self):
        values = request.values
        if not ('doc_id' in values):
            return 'Need id'
        if not ('type' in values):
            return 'Need type'
        title_book = self.controller.get_document(values.get('doc_id'), values.get('type'))['title']
        f, self.notification_id = self.controller.outstanding_request(values.get('doc_id'), values.get('type'))
        return "OK"
