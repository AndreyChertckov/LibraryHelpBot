from flask import Flask, request, redirect
from AdminSite.DBmanager import DBManager
import hashlib
import random
import base64


class API:

    def __init__(self, controller):
        self.app = Flask(__name__)
        self.cntrl = controller
        self.dbmanager = DBManager()
        self.init_handlers()
    
    def init_handlers(self):
        self.app.add_url_rule('/signin','signin',self.signin_post,methods=['POST'])
        self.app.add_url_rule('/signup','signup',self.signup_post,methods=['POST'])

    def run(self):
        self.app.run()

    def generate_sault(self):
        sault = bytes([random.randint(0,16) for i in range(16)])
        return base64.b64encode(sault)
        
    def create_session(self,login,passwd):
        hasher = hashlib.md5()
        hasher.update((login + passwd + self.generate_sault()).encode('utf-8'))
        user_id = self.dbmanager.get_user_id(login,passwd)[0]
        self.dbmanager.create_session(hasher.hexdigest(),user_id)
        return hasher.hexdigest()

    def signin_post(self):
        login = request.values.get('login')
        hasher = hashlib.md5()
        hasher.update(request.values.get('password').encode('utf-8'))
        passwd = hasher.hexdigest()
        if self.dbmanager.get_user(login,passwd) == None:
            return self.app.make_response(redirect('/signin'))

        response = self.app.make_response(redirect('/'))
        response.set_cookie('session_id',self.generate_sault())
        return response
    
    def signup_post(self):
        print(request.values)
        keys = ['login','name','phone','address']
        user = dict(zip(keys,[request.values.get(key) for key in keys]))
        hasher = hashlib.md5()
        hasher.update(request.values.get('password').encode('utf-8'))
        user['passwd'] = hasher.hexdigest()
        self.dbmanager.create_user(user)
        return 'OK'
        
    