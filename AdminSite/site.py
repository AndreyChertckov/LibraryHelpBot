from flask import Flask
from AdminSite.api import API


class Main:

    def __init__(self, controller):
        self.app = Flask(__name__)
        self.api = API(controller,self.app)
    
    def run(self):
        self.app.run(debug=True)
