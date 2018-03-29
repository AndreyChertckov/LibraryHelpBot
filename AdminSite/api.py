from flask import Blueprint, request, redirect,jsonify
from AdminSite.DBmanager import DBManager
import hashlib
import random
import base64


class API:

    def __init__(self, controller,app):
        self.blueprint = Blueprint('api',__name__)
        self.init_handlers()
        self.app = app
        self.app.register_blueprint(self.blueprint)
        self.controller = controller
        self.dbmanager = DBManager()

    def init_handlers(self):
        self.blueprint.add_url_rule('/signin','signin',self.signin_post,methods=['POST'])
        self.blueprint.add_url_rule('/signup','signup',self.signup_post,methods=['POST'])
        self.blueprint.add_url_rule('/signout','signout',self.signout_get,methods=['GET'])
        self.blueprint.add_url_rule('/api/get_all_unconfirmed','get_all_unconfirmed',self.get_all_unconfirmed_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/confirm_user','confirm_user',self.confirm_user_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/modify_user','modify_user',self.modify_user_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/delete_user','delete_user',self.delete_user_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_all_patrons','get_all_patrons',self.get_all_patrons_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_user','get_user',self.get_user_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_user_by_name','get_user_by_name',self.get_user_by_name_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/user_get_doc','user_get_doc',self.user_get_doc_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/return_doc','return_doc',self.return_doc_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_user_orders','get_user_orders',self.get_user_orders_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_order','get_order',self.get_order_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_all_orders','get_all_orders',self.get_all_orders_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_all_active_orders','get_all_active_orders',self.get_all_active_orders_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_all_whaiting_doc','get_all_whaiting_doc',self.get_all_whaiting_doc_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_all_returned_doc','get_all_returned_doc',self.get_all_returned_doc,methods=['POST'])
        self.blueprint.add_url_rule('/api/add_document','add_document',self.add_document_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/modify_document','modify_document',self.modify_docment_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/add_copies_of_doc','add_copies_of_doc',self.add_copies_of_book_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/delete_document','delete_document',self.delete_document_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_document','get_document',self.get_document_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_all_doctype','get_all_doctype',self.get_all_doctype_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_documents_by_title','get_documents_by_title',self.get_documents_by_title_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/get_documents_by_authors','get_documents_by_authors',self.get_documents_by_authors_post,methods=['POST'])

    def generate_sault(self):
        sault = bytes([random.randint(0,16) for i in range(16)])
        return base64.b64encode(sault)

    def create_session(self,login,passwd):
        hasher = hashlib.md5()
        hasher.update((login + str(passwd) + str(self.generate_sault())).encode('utf-8'))
        user_id = self.dbmanager.get_user_id(login,passwd)[0]
        self.dbmanager.create_session(hasher.hexdigest(),user_id)
        return hasher.hexdigest()

    def check_session(self, session_id):
        return self.dbmanager.get_user_id_by_session(session_id) != None

    def signin_post(self):
        login = request.values.get('login')
        hasher = hashlib.md5()
        hasher.update(request.values.get('password').encode('utf-8'))
        passwd = hasher.hexdigest()
        if self.dbmanager.get_user(login,passwd) == None:
            return redirect('/signin')
        response = self.app.make_response(redirect('/'))
        response.set_cookie('session_id',self.create_session(login,passwd))
        return response

    def signup_post(self):
        keys = ['login','name','phone','address']
        user = dict(zip(keys,[request.values.get(key) for key in keys]))
        hasher = hashlib.md5()
        hasher.update(request.values.get('password').encode('utf-8'))
        user['passwd'] = hasher.hexdigest()
        self.dbmanager.create_user(user)
        response = self.app.make_response(redirect('/'))
        response.set_cookie('session_id',self.create_session(user['login'],user['passwd']))
        return response

    def signout_get(self):
        session_id = request.cookies['session_id']
        self.dbmanager.delete_session(session_id)
        response = self.app.make_response(redirect('/'))
        response.set_cookie('session_id', '', expires=0)
        return response

    def get_all_unconfirmed_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('session_id')):
            return jsonify(self.controller.get_all_unconfirmed())
        else:
            return 'Sign in before'
    
    def confirm_user_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('session_id')):
            if 'user_id' in request.values:
                user_id = request.values.get('user_id')
                return 'OK'
            else:
                return 'Need id of user'
        else:
            return 'Sign in before'
    
    def modify_user_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('seesion_id')):
            keys = ['id','name','phone','address','status']
            user = {}
            for key in keys:
                if key in request.values:
                    user[key] = request.values.get(key)
            if not 'id' in user:
                return 'Need id'
            self.controller.modify_user(user)
            return 'OK'
        else:
            return 'Sign in before'
    
    def delete_user_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('session_id')):
            if 'user_id' in request.values:
                self.controller.delete_user(request.values.get('user_id'))
                return 'OK'
            else:
                return 'Need id of user'
        else:
            return 'Sign in before'
    
    def get_all_patrons_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('session_id')):
            return jsonify(self.controller.get_all_patrons())
        else:
            return 'Sign in before'
    
    
    def get_user_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('session_id')):
            if 'user_id' in request.values:
                return jsonify(self.controller.get_user(request.values.get('user_id')))
            else:
                return 'Need id of user'
        else:
            return 'Sign in before'
    
    def get_user_by_name_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('session_id')):
            if 'name' in request.values:
                return jsonify(self.controller.get_user_by_name(request.values.get('name')))
            else:
                return 'Need id of user'
        else:
            return 'Sign in before'
    
    def user_get_doc_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('session_id')):
            if 'order_id' in request.values:
                self.controller.user_get_doc(request.cookies.get('session_id'))
                return 'OK'
            else:
                return 'Need id of order'
        else:
            return 'Sign in before'
    
    def return_doc_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('session_id')):
            if 'order_id' in request.values:
                self.controller.return_doc(request.cookies.get('order_id'))
                return 'OK'
            else:
                return 'Need id of order'
        else:
            return 'Sign in before'
    
    def get_user_orders_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('session_id')):
            if 'user_id' in request.values:
                return jsonify(self.controller.get_user_orders(request.values.get('user_id')))
            else:
                return 'Need id of user'
        else:
            return 'Sign in before'
    
    def get_order_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('session_id')):
            if 'order_id' in request.values:
                return jsonify(self.controller.get_order(request.values.get('order_id')))
            else:
                return 'Need id of order'
        else:
            return 'Sign in before'

    def get_all_orders_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('session_id')):
            return jsonify(self.controller.get_all_orders())
        else:
            return 'Sign in before'
    
    def get_all_active_orders_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('session_id')):
            return jsonify(self.controller.get_all_activate_orders())
        else:
            return 'Sign in before'
    
    def get_all_whaiting_doc_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('session_id')):
            return jsonify(self.controller.get_all_whaiting_doc())
        else:
            return 'Sign in before'
    
    def get_all_returned_doc(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('session_id')):
            return jsonify(self.controller.get_all_returned_doc())
        else:
            return 'Sign in before'
    
    def add_document_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('session_id')):
            document = []
            keys = ['title','description','authors','count','price','keywords','best_seller']
            doc_type = request.values.get('doc_type')
            if doc_type == 'article':
                keys.extend(['journal','issue','editors','date'])
            if all([key in request.values for key in keys]):
                document = dict(zip(keys,[request.values.get(key) for key in keys]))
                self.controller.add_document(document,doc_type)
                return 'OK'
            else:
                return 'Not enough keys'
        else:
            return 'Sign in before'
    
    def modify_docment_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('seesion_id')):
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
    
    def add_copies_of_book_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('seesion_id')):
            if not 'id' in request.values:
                return 'Need id'
            if not 'delta_count' in request.values:
                return 'Need delta count'
            if not 'type' in request.values:
                return 'Need type'
            self.controller.add_copies_of_book(request.values.get('type'),request.values.get('id'),request.values.get('delta_count'))
            return 'OK'
        else:
            return 'Sign in before'
    
    def delete_document_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('seesion_id')):
            if not 'id' in request.values:
                return 'Need id'
            if not 'type' in request.values:
                return 'Need type'
            self.controller.delete_document(request.values.get('id'),request.values.get('type'))
            return 'OK'
        else:
            return 'Sign in before'
    
    def get_document_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('seesion_id')):
            if not 'id' in doc:
                return 'Need id'
            if not 'type' in request.values:
                return 'Need type'
            return jsonify(self.controller.get_document(request.values.get('id'),request.values.get('type')))
        else:
            return 'Sign in before'

    def get_all_doctype_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('seesion_id')):
            if not 'type' in request.values:
                return 'Need type'
            return jsonify(self.controller.get_all_doctype(request.values.get('type')))
        else:
            return 'Sign in before'
    
    def get_documents_by_title_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('seesion_id')):
            if not 'title' in request.values:
                return 'Need title'
            if not 'type' in request.values:
                return 'Need type'
            return jsonify(self.controller.get_documents_by_title(request.values.get('title'),request.values.get('type')))
        else:
            return 'Sign in before'
    
    def get_documents_by_authors_post(self):
        if 'session_id' in request.cookies and self.check_session(request.cookies.get('seesion_id')):
            if not 'authors' in request.values:
                return 'Need authors'
            if not 'type' in request.values:
                return 'Need type'
            return jsonify(self.controller.get_documents_by_title(request.values.get('authors'),request.values.get('type')))
        else:
            return 'Sign in before'