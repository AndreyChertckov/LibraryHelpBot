from flask import Flask, request
from AdminSite.DBmanager import DBManager
import hashlib


class API:

    def __init__(self, controller):
        self.app = Flask(__name__)
        self.cntrl = controller
        self.dbmanager = DBManager()
        self.init_handlers()
    
    def init_handlers(self):
        self.app.add_url_rule('/login','login',self.signin_post,methods=['POST'])

    def run(self):
        self.app.run()

    def signin_post(self):
        login = request.values.get('login')
        hasher = hashlib.md5()
        hasher.update(request.values.get('password').encode('utf-8'))
        passwd = hasher.hexdigest()
        if self.dbmanager.get_user(login,passwd) == None:
            return 'Invalid login or password'
        return 'HELLO WORLD'
    
    def signup_post(self):
        pass
    