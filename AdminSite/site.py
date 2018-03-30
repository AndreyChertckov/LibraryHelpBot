from flask import Flask
from AdminSite.api import API
from AdminSite.views import Views
from AdminSite.DBmanager import DBManager

class Main:

    def __init__(self, controller):
        self.app = Flask(__name__)
        self.dbmanager = DBManager()
        self.api = API(self.app,controller,self.dbmanager)
        self.views = Views(self.app,self.api,self.dbmanager)
    
    def run(self):
        self.app.run(threaded=True)
