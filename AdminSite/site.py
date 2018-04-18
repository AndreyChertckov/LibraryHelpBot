from flask import Flask
from AdminSite.api import API
from AdminSite.views import Views
from AdminSite.DBmanager import DBManager
from AdminSite.notification import Notification

from configs import admin_user_login, admin_user_pass, host, port, debug
from AdminSite.utils import md5_hash

import ssl


class Main:

    def __init__(self, controller, bot):
        self.app = Flask(__name__)
        self.dbmanager = DBManager()
        self.notification = Notification(bot)
        self.api = API(self.app, controller, self.dbmanager, self.notification)
        self.views = Views(self.app, self.api, self.dbmanager)
        self.create_admin_user()
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.load_cert_chain('ssl/libraryhelpbot.com.crt', 'ssl/libraryhelpbot.com.key')

    def create_admin_user(self):
        user = {'login': admin_user_login, 'name': 'Admin',
                'phone': '', 'address': '', 'privilege': '3'}
        user['passwd'] = md5_hash(admin_user_pass.encode('utf-8'))
        if not self.dbmanager.get_user_id(admin_user_login, user['passwd']):
            self.dbmanager.create_user(user)

    def run(self):
        self.app.run(threaded=True, host=host, port=int(port), debug=debug)
