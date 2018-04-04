from flask import Blueprint, request, redirect,jsonify
from AdminSite.utils import *

from configs import host, telegram_alias

class API:

    def __init__(self, app, controller,dbmanager,notification):
        self.blueprint = Blueprint('api',__name__)
        self.init_handlers()
        self.app = app
        self.dbmanager = dbmanager
        self.app.register_blueprint(self.blueprint)
        self.controller = controller
        self.notifictation = notification

    def init_handlers(self):
        self.blueprint.add_url_rule('/signin','signin',self.signin_post,methods=['POST'])
        self.blueprint.add_url_rule('/signup','signup',self.signup_post,methods=['POST'])
        self.blueprint.add_url_rule('/signout','signout',self.signout_get,methods=['GET'])
        self.blueprint.add_url_rule('/api/get_verification_links','get_verification_links',self.get_verification_links,methods=['POST'])
        self.blueprint.add_url_rule('/api/generate_invite_link','generate_invite_link',self.generate_verification_string,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_telegram_verification_message','get_telegram_verification_message',self.get_telegram_verification_message_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_all_unconfirmed','get_all_unconfirmed',self.get_all_unconfirmed_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/confirm_user','confirm_user',self.confirm_user_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/modify_user','modify_user',self.modify_user_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/delete_user','delete_user',self.delete_user_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_all_patrons','get_all_patrons',self.get_all_patrons_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_all_librarians','get_all_librarians',self.get_all_librarians_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_librarian_by_name','get_librarian_by_name',self.get_librarian_by_name_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_user','get_user',self.get_user_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_user_by_name','get_user_by_name',self.get_user_by_name_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/user_get_doc','user_get_doc',self.user_get_doc_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/return_doc','return_doc',self.return_doc_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_user_orders','get_user_orders',self.get_user_orders_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_user_history','get_user_history',self.get_user_history_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_order','get_order',self.get_order_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_all_orders','get_all_orders',self.get_all_orders_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_all_active_orders','get_all_active_orders',self.get_all_active_orders_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_all_waiting_doc','get_all_waiting_doc',self.get_all_waiting_doc_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_all_returned_doc','get_all_returned_doc',self.get_all_returned_doc,methods=['POST'])
        self.blueprint.add_url_rule('/api/add_document','add_document',self.add_document_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/modify_document','modify_document',self.modify_docment_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/add_copies_of_doc','add_copies_of_doc',self.add_copies_of_doc_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/delete_document','delete_document',self.delete_document_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_document','get_document',self.get_document_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_all_doctype','get_all_doctype',self.get_all_doctype_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_documents_by_title','get_documents_by_title',self.get_documents_by_title_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_documents_by_authors','get_documents_by_authors',self.get_documents_by_authors_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_queue_on_document','get_queue_on_document',self.get_queue_on_documnent_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/outstanding','outstanding',self.outstanding_post,methods=['POST'])

    def signin_post(self):
        login = request.values.get('login')
        passwd = md5_hash(request.values.get('password').encode('utf-8'))
        if self.dbmanager.get_user(login,passwd) == None:
            response = self.app.make_response(redirect('/signin'))
            response.set_cookie('error', 'Login error')
            return response
        response = self.app.make_response(redirect('/'))
        response.set_cookie('session_id',create_session(login,passwd,self.dbmanager))
        return response

    def generate_verification_string(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            string = md5_hash(generate_sault())
            self.dbmanager.insert_verification_string(string)
            return string
        else:
            return 'Sign in before'
    
    def get_verification_links(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            link = "http://"+host + '/signup?verification_string='
            ver_strings = self.dbmanager.all_verification_strings(1)
            if ver_strings:
                output = [link+string[0] for string in ver_strings]
                return jsonify(output)
            else:
                return jsonify([])
        else:
            return 'Sign in before'

    def get_telegram_verification_message_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            session_id = request.cookies.get('session_id')
            user_id = self.dbmanager.get_user_id_by_session(session_id)
            ver_val = self.dbmanager.get_verification_string(user_id)
            return 'Write to telegram bot(<a href="https://t.me/{}">https://t.me/{}</a>) this line</br> /verification {}'.format(telegram_alias,telegram_alias,ver_val[0])
        else:
            return 'Sign in before'

    def signup_post(self):
        print(request.values)
        if 'verification_string' in request.values and self.dbmanager.if_verification_string_exist(request.values.get('verification_string'),1):
            keys = ['login','name','phone','address']
            user = dict(zip(keys,[request.values.get(key) for key in keys]))
            user['passwd'] = md5_hash(request.values.get('password').encode('utf-8'))
            self.dbmanager.create_user(user)
            response = self.app.make_response(redirect('/'))
            session_id = create_session(user['login'],user['passwd'],self.dbmanager)
            response.set_cookie('session_id',session_id)
            user_id = self.dbmanager.get_user_id_by_session(session_id)
            self.dbmanager.activate_verification_string(request.values.get('verification_string'),user_id)
            return response
        else:
            return 'Please write to another librarian to get signup link.'

    def signout_get(self):
        session_id = request.cookies['session_id']
        self.dbmanager.delete_session(session_id)
        response = self.app.make_response(redirect('/'))
        response.set_cookie('session_id', '', expires=0)
        return response

    def get_all_unconfirmed_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            return jsonify(self.controller.get_all_unconfirmed())
        else:
            return 'Sign in before'
    
    def confirm_user_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            if 'user_id' in request.values:
                user_id = request.values.get('user_id')
                success = self.controller.confirm_user(user_id)
                self.notifictation.send_message(user_id,"Your application was confirmed.")
                return 'OK' if success else "Somthing went wrong"
            else:
                return 'Need id of user'
        else:
            return 'Sign in before'
    
    def modify_user_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            keys = ['id','name','phone','address','status']
            user = {}
            for key in keys:
                if key in request.values:
                    user[key] = request.values.get(key)
            if not 'id' in user:
                print(user)
                return 'Need id'
            print(user)
            self.controller.modify_user(user)
            return 'OK'
        else:
            return 'Sign in before'
    
    def delete_user_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            if 'user_id' in request.values:
                self.notifictation.send_message(request.values.get('user_id'),"Your account was deleted.")
                return str(self.controller.delete_user(request.values.get('user_id')))
            else:
                return 'Need id of user'
        else:
            return 'Sign in before'
    
    def get_all_patrons_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            return jsonify(self.controller.get_all_patrons())
        else:
            return 'Sign in before'
    
    def get_all_librarians_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            librarians_list = [dict(zip(['id','name','phone','address'],tup)) for tup in self.dbmanager.get_users()]
            return jsonify(librarians_list)
        else:
            return 'Sign in before'
    
    def get_librarian_by_name_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            librarians_list = dict(zip(('id','name','phone','address'),self.dbmanager.get_user_by_name(request.values.get('name'))))
            return jsonify(librarians_list)
        else:
            return 'Sign in before'
    
    def get_user_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            if 'user_id' in request.values:
                return jsonify(self.controller.get_user(request.values.get('user_id')))
            else:
                return 'Need id of user'
        else:
            return 'Sign in before'
    
    def get_user_by_name_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            if 'name' in request.values:
                return jsonify(self.controller.get_user_by_name(request.values.get('name')))
            else:
                return 'Need id of user'
        else:
            return 'Sign in before'
    
    def user_get_doc_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            if 'order_id' in request.values:
                self.controller.user_get_doc(request.values.get('order_id'))
                return 'OK'
            else:
                return 'Need id of order'
        else:
            return 'Sign in before'
    
    def return_doc_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            if 'order_id' in request.values:
                title_doc = self.controller.get_order(request.values.get('order_id'))['doc']['title']
                _,_,_,user_for_notify = self.controller.return_doc(request.values.get('order_id'))
                if user_for_notify != -1:
                    self.notifictation.send_message(user_for_notify,"You can get document "+title_doc)
            else:
                return 'Need id of order'
        else:
            return 'Sign in before'
    
    def get_user_orders_post(self):
        if 'session_id' in request.cookies and check_session(request.co']
                _,_,_,user_for_notify = self.controller.return_doc(request.values.get('order_id'))
                self.notifictation.send_message(user_for_notify,"You can get document "+title_doc)
            else:
                return 'Need id of order'
        else:
            return 'Sign in before'
    
    def get_user_orders_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            if 'user_id' in request.values:
                return jsonify(self.controller.get_user_orders(request.values.get('user_id')))
            else:
                return 'Need id of user'
        else:
            return 'Sign in before'
    
    def get_user_history_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            if 'user_id' in request.values:
                return jsonify(self.controller.get_user_history(request.values.get('user_id')))
            else:
                return 'Need id of user'
        else:
            return 'Sign in before'
    
    def get_order_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            if 'order_id' in request.values:
                return jsonify(self.controller.get_order(request.values.get('order_id')))
            else:
                return 'Need id of order'
        else:
            return 'Sign in before'

    def get_all_orders_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            return jsonify(self.controller.get_all_orders())
        else:
            return 'Sign in before'
    
    def get_all_active_orders_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            return jsonify(self.controller.get_all_active_orders())
        else:
            return 'Sign in before'
    
    def get_all_waiting_doc_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            return jsonify(self.controller.get_all_waiting_doc())
        else:
            return 'Sign in before'
    
    def get_all_returned_doc(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            return jsonify(self.controller.get_all_returned_orders())
        else:
            return 'Sign in before'
    
    def add_document_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            document = []
            keys = ['title','description','authors','count','price','keywords','best_seller','free_count']
            doc_type = request.values.get('type')
            if doc_type == 'article':
                keys.extend(['journal','issue','editors','date'])
            if all([key in request.values for key in keys]):
                document = dict(zip(keys,[request.values.get(key) if key != "best_seller" else int(request.values.get(key)) for key in keys]))
                print(document)
                self.controller.add_document(document,doc_type)
                return 'OK'
            else:
                print([key for key in request.values.keys()])
                return 'Not enough keys'
        else:
            return 'Sign in before'
    
    def modify_docment_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            keys = ['id','title','authors','description','price','best_seller','keywords','journal','issue','editors','date']
            doc = {}
            for key in keys:
                if key in request.values:
                    doc[key] = request.values.get(key)
            if not 'id' in doc:
                return 'Need id'
            if not 'type' in request.values:
                return 'Need type'
            self.controller.modify_document(doc,request.values.get('type'))
            return 'OK'
        else:
            return 'Sign in before'
    
    def add_copies_of_doc_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            if not 'id' in request.values:
                return 'Need id'
            if not 'delta_count' in request.values:
                return 'Need delta count'
            if not 'type' in request.values:
                return 'Need type'
            self.controller.add_copies_of_document(request.values.get('type'),request.values.get('id'),int(request.values.get('delta_count')))
            return 'OK'
        else:
            return 'Sign in before'
    
    def delete_document_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            if not 'id' in request.values:
                return 'Need id'
            if not 'type' in request.values:
                return 'Need type'
            self.controller.delete_document(request.values.get('id'),request.values.get('type'))
            return 'OK'
        else:
            return 'Sign in before'
    
    def get_document_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            if not 'id' in request.values:
                return 'Need id'
            if not 'type' in request.values:
                return 'Need type'
            return jsonify(self.controller.get_document(request.values.get('id'),request.values.get('type')))
        else:
            return 'Sign in before'

    def get_all_doctype_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            if not 'type' in request.values:
                return 'Need type'
            return jsonify(self.controller.get_all_doctype(request.values.get('type')))
        else:
            return 'Sign in before'
    
    def get_documents_by_title_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            if not 'title' in request.values:
                return 'Need title'
            if not 'type' in request.values:
                return 'Need type'
            return jsonify(self.controller.get_documents_by_title(request.values.get('title'),request.values.get('type')))
        else:
            return 'Sign in before'
    
    def get_documents_by_authors_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            if not 'authors' in request.values:
                return 'Need authors'
            if not 'type' in request.values:
                return 'Need type'
            return jsonify(self.controller.get_documents_by_title(request.values.get('authors'),request.values.get('type')))
        else:
            return 'Sign in before'
    
    def get_queue_on_documnent_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            if not 'doc_id' in request.values:
                return 'Need id'
            if not 'type' in request.values:
                return 'Need type'
            return jsonify(self.controller.get_document_queue(request.values.get('type'),request.values.get('doc_id')))
        else:
            return 'Sign in before'
    
    def outstanding_post(self):
        if 'session_id' in request.cookies and check_session(request.cookies.get('session_id'),self.dbmanager):
            if not 'doc_id' in request.values:
                return 'Need id'
            if not 'type' in request.values:
                return 'Need type'
            title_book = self.controller.get_document(request.values.get('doc_id'),request.values.get('type'))['title']
            f,notify_users = self.controller.outstanding_request(request.values.get('doc_id'),request.values.get('type'))
            print(f,notify_users)
            for user in notify_users:
                self.notifictation.send_message(user,"Please return document " + title_book)
            return "OK"
        else:
            return 'Sign in before'